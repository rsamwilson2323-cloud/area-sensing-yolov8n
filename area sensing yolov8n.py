import cv2
import numpy as np
import copy
from ultralytics import YOLO

# ================= CONFIG =================
MODEL_PATH = "yolov8n.pt"
RUN_EVERY_N_FRAMES = 3      # speed control
ZONE_ALPHA = 0.35
DRAG_THRESHOLD = 6
CONFIDENCE = 0.4           # all 80 classes

# ================= LOAD MODEL =================
model = YOLO(MODEL_PATH)

# ================= GLOBAL STATE =================
zones = []
current_points = []
preview_point = None

undo_stack = []
redo_stack = []

lmb_down = False
rmb_down = False
dragging = False
start_pos = None

drawing_circle = False
drawing_rect = False
dragging_zone = False

circle_center = None
circle_radius = 0
rect_start = None
rect_end = None

selected_zone = None
drag_start = None

frame_count = 0
last_results = None   # prevents blinking

# ================= UNDO / REDO =================
def save_state():
    undo_stack.append(copy.deepcopy(zones))
    redo_stack.clear()

def undo():
    global zones
    if undo_stack:
        redo_stack.append(copy.deepcopy(zones))
        zones = undo_stack.pop()

def redo():
    global zones
    if redo_stack:
        undo_stack.append(copy.deepcopy(zones))
        zones = redo_stack.pop()

# ================= POLYGON CLOSURE CHECK =================
def is_polygon_closed(frame_shape, points):
    mask = np.zeros(frame_shape[:2], np.uint8)
    cv2.polylines(mask, [np.array(points)], False, 255, 2)
    flood = mask.copy()
    cv2.floodFill(flood, None, (0, 0), 255)
    inv = cv2.bitwise_not(flood)
    return cv2.countNonZero(inv) > 0

# ================= MOUSE HANDLER =================
def mouse_event(event, x, y, flags, param):
    global lmb_down, rmb_down, dragging, start_pos
    global drawing_circle, drawing_rect
    global circle_center, circle_radius
    global rect_start, rect_end
    global current_points, preview_point
    global selected_zone, dragging_zone, drag_start

    # ---- BUTTON DOWN ----
    if event == cv2.EVENT_LBUTTONDOWN:
        lmb_down = True
        start_pos = (x, y)
        dragging = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        rmb_down = True
        start_pos = (x, y)
        dragging = False

    elif event == cv2.EVENT_MBUTTONDOWN:
        for i, z in enumerate(zones):
            inside = False
            if z["type"] == "polygon":
                inside = cv2.pointPolygonTest(np.array(z["points"]), (x, y), False) >= 0
            elif z["type"] == "circle":
                cx, cy = z["center"]
                inside = np.hypot(x - cx, y - cy) <= z["radius"]
            elif z["type"] == "rect":
                xs = [p[0] for p in z["points"]]
                ys = [p[1] for p in z["points"]]
                inside = min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys)

            if inside:
                selected_zone = i
                dragging_zone = True
                drag_start = (x, y)
                break

    # ---- MOVE ----
    elif event == cv2.EVENT_MOUSEMOVE:
        preview_point = (x, y)

        if (lmb_down or rmb_down) and not dragging:
            if abs(x - start_pos[0]) > DRAG_THRESHOLD or abs(y - start_pos[1]) > DRAG_THRESHOLD:
                dragging = True
                if lmb_down:
                    drawing_circle = True
                    circle_center = start_pos
                if rmb_down:
                    drawing_rect = True
                    rect_start = start_pos
                    rect_end = start_pos

        if drawing_circle:
            circle_radius = int(np.hypot(x - circle_center[0], y - circle_center[1]))

        if drawing_rect:
            rect_end = (x, y)

        if dragging_zone and selected_zone is not None:
            dx = x - drag_start[0]
            dy = y - drag_start[1]
            z = zones[selected_zone]

            if z["type"] == "polygon":
                z["points"] = [(px + dx, py + dy) for px, py in z["points"]]
            elif z["type"] == "circle":
                cx, cy = z["center"]
                z["center"] = (cx + dx, cy + dy)
            elif z["type"] == "rect":
                z["points"] = [(px + dx, py + dy) for px, py in z["points"]]

            drag_start = (x, y)

    # ---- BUTTON UP ----
    elif event == cv2.EVENT_LBUTTONUP:
        lmb_down = False
        if drawing_circle:
            if circle_radius > DRAG_THRESHOLD:
                save_state()
                zones.append({
                    "type": "circle",
                    "center": circle_center,
                    "radius": circle_radius
                })
            drawing_circle = False
        else:
            current_points.append((x, y))

    elif event == cv2.EVENT_RBUTTONUP:
        rmb_down = False
        if drawing_rect:
            save_state()
            x1, y1 = rect_start
            x2, y2 = rect_end
            zones.append({
                "type": "rect",
                "points": [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
            })
            drawing_rect = False
        else:
            if len(current_points) >= 3:
                if is_polygon_closed(frame.shape, current_points):
                    save_state()
                    zones.append({
                        "type": "polygon",
                        "points": current_points.copy()
                    })
                    current_points.clear()

    elif event == cv2.EVENT_MBUTTONUP:
        dragging_zone = False
        selected_zone = None

# ================= UTILITIES =================
def inside_zone(cx, cy, z):
    if z["type"] == "polygon":
        return cv2.pointPolygonTest(np.array(z["points"]), (cx, cy), False) >= 0
    if z["type"] == "circle":
        x, y = z["center"]
        return np.hypot(cx - x, cy - y) <= z["radius"]
    if z["type"] == "rect":
        xs = [p[0] for p in z["points"]]
        ys = [p[1] for p in z["points"]]
        return min(xs) <= cx <= max(xs) and min(ys) <= cy <= max(ys)

def draw_zone(frame, z):
    overlay = frame.copy()
    color = (0, 255, 0)
    if z["type"] == "polygon":
        pts = np.array(z["points"])
        cv2.fillPoly(overlay, [pts], color)
        cv2.polylines(frame, [pts], True, color, 2)
    elif z["type"] == "circle":
        cv2.circle(overlay, z["center"], z["radius"], color, -1)
        cv2.circle(frame, z["center"], z["radius"], color, 2)
    elif z["type"] == "rect":
        pts = np.array(z["points"])
        cv2.fillPoly(overlay, [pts], color)
        cv2.polylines(frame, [pts], True, color, 2)
    return cv2.addWeighted(overlay, ZONE_ALPHA, frame, 1 - ZONE_ALPHA, 0)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

cv2.namedWindow("AREA SENSING YOLO", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AREA SENSING YOLO",
                      cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("AREA SENSING YOLO", mouse_event)

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()

    for z in zones:
        display = draw_zone(display, z)

    for i in range(1, len(current_points)):
        cv2.line(display, current_points[i-1], current_points[i], (255,255,255), 2)
    if current_points and preview_point:
        cv2.line(display, current_points[-1], preview_point, (180,180,180), 1)

    if drawing_circle:
        cv2.circle(display, circle_center, circle_radius, (255,255,0), 2)
    if drawing_rect:
        cv2.rectangle(display, rect_start, rect_end, (255,0,0), 2)

    frame_count += 1
    if frame_count % RUN_EVERY_N_FRAMES == 0:
        small = cv2.resize(frame, (640, 480))
        last_results = model(
            small,
            conf=CONFIDENCE,
            verbose=False
        )[0]

    if last_results:
        sx = frame.shape[1] / 640
        sy = frame.shape[0] / 480
        for box in last_results.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1*sx), int(y1*sy), int(x2*sx), int(y2*sy)
            cx,cy = (x1+x2)//2, (y1+y2)//2

            if not any(inside_zone(cx, cy, z) for z in zones):
                continue

            cv2.rectangle(display,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.putText(display,label,(x1,y1-8),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)

    cv2.imshow("AREA SENSING YOLO", display)

    key = cv2.waitKey(1)
    if key == 13:  # ENTER
        break
    if key == 26:  # Ctrl+Z
        undo()
    if key == 25:  # Ctrl+Y
        redo()

cap.release()
cv2.destroyAllWindows()
