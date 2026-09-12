"""Render the static career map. No runtime dependencies or interaction."""
from pathlib import Path

WIDTH, HEIGHT = 720, 270
faces = []


def project(x, z, y=0):
    return 360 + x * 1.12 + z * .55, 187 + z * .45 - x * .13 - y, z + y * .5


def polygon(points, color):
    p = [project(*v) for v in points]
    shape = '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y, _ in p) + f'" fill="{color}"/>'
    faces.append((sum(v[2] for v in p) / len(p), shape))


def block(x, z, y, width, depth, height, top, front, side):
    a = [x-width/2, z-depth/2, y]
    b = [x+width/2, z-depth/2, y]
    c = [x+width/2, z+depth/2, y]
    d = [x-width/2, z+depth/2, y]
    A, B, C, D = [[*v[:2], y+height] for v in [a, b, c, d]]
    for points, color in [([a,b,B,A],side),([a,d,D,A],front),([d,c,C,D],front),([b,c,C,B],side),([A,B,C,D],top)]:
        polygon(points, color)


# One continuous, shallow landform; the route is read from left to right.
block(0, 5, -17, 470, 138, 12, '#283e39', '#1a2c28', '#20332e')
block(0, 5, -5, 470, 138, 5, '#3b5148', '#2a3d35', '#30483d')
# The light paving passes in front of the campus and turns toward the office.
block(-57, 42, 0, 310, 28, 3, '#b8b5a1', '#828b79', '#9ca48d')
block(103, 12, 0, 28, 88, 3, '#b8b5a1', '#828b79', '#9ca48d')
block(146, -18, 0, 105, 28, 3, '#b8b5a1', '#828b79', '#9ca48d')
for x in [-175,-145,-115,-85,-55,-25,5,35,65]:
    block(x,42,3,10,2,1,'#f3edda','#f3edda','#f3edda')
for z in [-11,12,35]:
    block(103,z,3,2,10,1,'#f3edda','#f3edda','#f3edda')
for x in [125,153,181]:
    block(x,-18,3,10,2,1,'#f3edda','#f3edda','#f3edda')
terrain = sorted(faces)
faces.clear()

# Campus: a low cream building with a broad roof and entrance columns.
x,z=-158,-12
block(x,z,0,100,80,5,'#9eab93','#647461','#83907b')
block(x,z,5,72,44,36,'#eee3ca','#b9aa8e','#d4c7ad')
block(x,z,41,82,53,6,'#f4e9d3','#b9a786','#d8c6a5')
block(x,z-8,47,43,25,12,'#f0c994','#ab8359','#d0a877')
block(x,z-8,59,51,31,4,'#f3d7af','#b59a77','#d8bc94')
for dx in [-23,-8,8,23]:
    block(x+dx,z+27,6,6,8,34,'#f7ead1','#c1b299','#e2d4bb')
# Office: restrained height and flat pastel glass, without a selected state.
x,z=160,-30
block(x,z,0,100,82,5,'#a6bbae','#657f6c','#89a491')
block(x-9,z,5,47,42,70,'#dce4e8','#8496b1','#abbcce')
block(x+27,z+4,5,24,36,38,'#d7e4df','#8caaa7','#abc4bb')
for level in range(5):
    block(x-9,z+22,17+level*11,35,1,4,'#dcecef','#dcecef','#bfd2df')
block(x-9,z,75,54,48,5,'#e9edef','#a1b2c0','#c5d0d8')
# Small shrubs give the path a map-like setting.
for x,z in [(-213,-45),(-210,7),(-69,-39),(-47,-44),(13,-45),(222,17),(218,-49)]:
    block(x,z,0,17,17,5,'#8aa982','#455f4c','#648260')
    block(x,z,5,21,20,14,'#b0c69b','#637f5e','#8caa78')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
    '<title id="title">학교에서 회사로 이어지는 2.5D 지도</title>',
    '<desc id="desc">학교와 회사 건물을 하나의 길로 연결한 정적인 입체 지도입니다. 이력과 로고는 README의 HTML에 별도로 표시합니다.</desc>',
    '<rect width="720" height="270" rx="10" fill="#11191d"/>',
]
parts.extend(shape for _, shape in terrain)
parts.extend(shape for _, shape in sorted(faces))
parts.append('</svg>')
output = Path(__file__).resolve().parents[1] / 'assets/profile/career-map-scene.svg'
output.write_text('\n'.join(parts))
print(output)
