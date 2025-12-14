import numpy as np
import matplotlib.pyplot as plt

#T(1), B(2), R(4), L(8)
INSIDE = 0  # 0000
TOP = 1     # 0001
BOTTOM = 2  # 0010
RIGHT = 4   # 0100
LEFT = 8    # 1000
#for creating window
X_MIN, Y_MIN = 15, 15
X_MAX, Y_MAX = 60, 60

def compute_outcode(x, y):
    code = INSIDE
    if x < X_MIN:
        code |= LEFT
    elif x > X_MAX:
        code |= RIGHT
    if y < Y_MIN:
        code |= BOTTOM
    elif y > Y_MAX:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_outcode(x1, y1)
    code2 = compute_outcode(x2, y2)
    
    original_points = [(x1, y1), (x2, y2)]
    print(f"Window: ({X_MIN},{Y_MIN}) to ({X_MAX},{Y_MAX})")
    print(f"P1({x1}, {y1}) output code: {code1:04b} (Decimal: {code1})")
    print(f"P2({x2}, {y2}) output code: {code2:04b} (Decimal: {code2})")
    accept = False
    
    while True:
        if code1 == INSIDE and code2 == INSIDE:
            accept = True
            break
        elif (code1 & code2) != INSIDE:
            break
        else:
            code_out = code1 if code1 != INSIDE else code2
            x, y = 0, 0
            
            # Calculate points
            if x2 != x1:
                m = (y2 - y1) / (x2 - x1)
            else:
                m = float('inf') 
            if code_out & TOP:
                x = x1 + (X_MAX if m == float('inf') else (Y_MAX - y1) / m)
                y = Y_MAX
            elif code_out & BOTTOM:
                x = x1 + (X_MIN if m == float('inf') else (Y_MIN - y1) / m)
                y = Y_MIN
            elif code_out & RIGHT:
                y = y1 + m * (X_MAX - x1)
                x = X_MAX
            elif code_out & LEFT:
                y = y1 + m * (X_MIN - x1)
                x = X_MIN
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_outcode(x2, y2)


    fig, ax = plt.subplots()
    ax.set_title("Cohen-Sutherland Line Clipping")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # Plot
    window_x = [X_MIN, X_MAX, X_MAX, X_MIN, X_MIN]
    window_y = [Y_MIN, Y_MIN, Y_MAX, Y_MAX, Y_MIN]
    ax.plot(window_x, window_y, 'b--', label='Clipping Window')
    ax.fill(window_x, window_y, 'b', alpha=0.1)
    all_coords = [original_points[0][0], original_points[0][1], original_points[1][0], original_points[1][1], X_MAX, Y_MAX]
    limit = max(all_coords) * 1.2
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_aspect('equal', adjustable='box')

    if accept:
        print(f"\nLine is PARTIALLY VISIBLE (Clipped)")
        print(f"Clipped Segment: P1'({x1:.2f}, {y1:.2f}) to P2'({x2:.2f}, {y2:.2f})")
        ax.plot([original_points[0][0], original_points[1][0]], 
                [original_points[0][1], original_points[1][1]], 
                'r-', alpha=0.3, label='Original Line')
        ax.plot([x1, x2], [y1, y2], 'g-', linewidth=2, label='Clipped Segment')
        ax.scatter([x1, x2], [y1, y2], color='g', marker='o')

    else:
        print("\nLine is NOT VISIBLE (Trivially Rejected)")
        ax.plot([original_points[0][0], original_points[1][0]], 
                [original_points[0][1], original_points[1][1]], 
                'r--', label='Rejected Line')

    ax.legend()
    plt.grid(True)
    plt.show()
    
    return x1, y1, x2, y2

P1_X, P1_Y = 20, 70
P2_X, P2_Y = 70, 20
clipped_x1, clipped_y1, clipped_x2, clipped_y2 = cohen_sutherland_clip(P1_X, P1_Y, P2_X, P2_Y)

#Made by: Remeah saad
#444500180



