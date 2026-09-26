# Simple collision simulation for level2 walls
walls = [[35, 35, 5, 100], [110, 0, 5, 40], [160, 40, 80, 5], [75, 60, 5, 35], [75, 90, 40, 5], [160, 90, 5, 45]]
radius = 7
step = 2


def circle_rect_collision(cx, cy, r, rx, ry, rw, rh):
    closest_x = rx if cx < rx else (rx + rw if cx > rx + rw else cx)
    closest_y = ry if cy < ry else (ry + rh if cy > ry + rh else cy)
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx * dx + dy * dy) <= (r * r)


def will_collide_at(x, y):
    cx = x + radius
    cy = y + radius
    for i, w in enumerate(walls):
        if circle_rect_collision(cx, cy, radius, w[0], w[1], w[2], w[3]):
            return True, i
    return False, None


def simulate(start_x, start_y, direction, limit=1000):
    x = start_x
    y = start_y
    steps = 0
    collided = False
    wall_idx = None
    while steps < limit:
        if direction == 'up':
            next_y = y - step
            coll, wi = will_collide_at(x, next_y)
            if coll or next_y < 0:
                collided = coll
                wall_idx = wi
                break
            y = next_y
        elif direction == 'down':
            next_y = y + step
            coll, wi = will_collide_at(x, next_y)
            if coll or next_y > 200:
                collided = coll
                wall_idx = wi
                break
            y = next_y
        elif direction == 'left':
            next_x = x - step
            coll, wi = will_collide_at(next_x, y)
            if coll or next_x < 0:
                collided = coll
                wall_idx = wi
                break
            x = next_x
        elif direction == 'right':
            next_x = x + step
            coll, wi = will_collide_at(next_x, y)
            if coll or next_x > 240:
                collided = coll
                wall_idx = wi
                break
        steps += 1
    return x, y, collided, wall_idx, steps


def run_tests():
    tests = [
        (110, 107, 'up'),
        (110, 107, 'down'),
        (110, 107, 'left'),
        (110, 107, 'right'),
        (12, 107, 'right'),
        (100, 80, 'left'),
    ]
    for sx, sy, dir in tests:
        x, y, c, wi, s = simulate(sx, sy, dir)
        print(f"Start=({sx},{sy}) Dir={dir} -> End=({x},{y}) Collided={c} WallIdx={wi} Steps={s}")

if __name__ == '__main__':
    run_tests()
