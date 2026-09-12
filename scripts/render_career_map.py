"""Render the static career map. No runtime dependencies or interaction."""
from pathlib import Path

WIDTH, HEIGHT = 720, 440
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

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
'<title id="title">하랑의 이력 지도</title>',
'<desc id="desc">동명대학교에서 디지털미디어공학과 융합미디어를 공부하고 졸업했습니다. 길은 현재 재직 중인 알파프라임으로 이어집니다. 프론트엔드 개발자로 제품을 만듭니다. 날짜와 인터랙션이 없는 정적인 지도입니다.</desc>',
'<rect width="720" height="440" rx="18" fill="#11191d"/>',
'<g font-family="Apple SD Gothic Neo,Malgun Gothic,Noto Sans KR,sans-serif">',
'<text x="34" y="45" fill="#a9b7b4" font-size="20">배움에서 제품을 만드는 일로</text>',
'<text x="686" y="45" text-anchor="end" fill="#7e9990" font-size="17">하랑의 이력 지도</text>']
parts.extend(shape for _, shape in terrain)
parts.extend(shape for _, shape in sorted(faces))
# Labels are always visible and contain the full career information.
parts.extend([
'<path d="M183 243V275M550 221V275" fill="none" stroke="#5c7669" stroke-width="1.5"/>',
'<circle cx="183" cy="275" r="3" fill="#d4bf9c"/><circle cx="550" cy="275" r="3" fill="#bdd9c8"/>',
'<text x="50" y="315" fill="#f0e4cc" font-size="28" font-weight="600">동명대학교</text>',
'<text x="50" y="352" fill="#b4c0bd" font-size="23">디지털미디어공학</text>',
'<text x="50" y="383" fill="#b4c0bd" font-size="23">융합미디어 · 졸업</text>',
'<text x="420" y="315" fill="#e4f0e8" font-size="28" font-weight="600">알파프라임</text>',
'<text x="420" y="352" fill="#b4c0bd" font-size="23">프론트엔드 개발자</text>',
'<circle cx="426" cy="375" r="4" fill="#a7dab6"/>',
'<text x="441" y="383" fill="#bce3c7" font-size="23">현재 재직 중</text>',
'</g></svg>'])
output = Path(__file__).resolve().parents[1] / 'assets/profile/career-map.svg'
output.write_text('\n'.join(parts))
print(output)
