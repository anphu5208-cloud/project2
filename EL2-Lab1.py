import sys
import heapq
from decimal import Decimal, getcontext

# Do chinh xac cao de cong cac so thap phan khong bi sai so nhu float
getcontext().prec = 50


def doc_so(s):
    """Doi chuoi thanh Decimal de tinh toan thap phan chinh xac (0.1 + 0.2 == 0.3)."""
    return Decimal(s)


def dinh_dang_so(x):
    """In so o dang thap phan, bo cac so 0 thua o cuoi (270 -> 270, 1.50 -> 1.5)."""
    d = Decimal(x)
    if d == d.to_integral_value():
        return str(int(d))
    return format(d.normalize(), "f")


def doc_du_lieu():
    """Doc toan bo stdin theo dang dong token (khong phu thuoc xuong dong)."""
    tokens = sys.stdin.read().split()
    pos = 0

    n = int(tokens[pos])
    pos += 1

    h = {}          # h[ten] = gia tri heuristic
    ke = {}         # ke[ten] = danh sach (lang_gieng, chi_phi)
    for _ in range(n):
        ten = tokens[pos]
        pos += 1
        h[ten] = doc_so(tokens[pos])
        pos += 1
        k = int(tokens[pos])
        pos += 1
        ds = []
        for _ in range(k):
            lg = tokens[pos]
            cp = doc_so(tokens[pos + 1])
            pos += 2
            ds.append((lg, cp))
        ke[ten] = ds

    f = int(tokens[pos])
    pos += 1
    vung_cam = set()
    for _ in range(f):
        vung_cam.add(tokens[pos])
        pos += 1

    start = tokens[pos]
    goal = tokens[pos + 1]
    return h, ke, vung_cam, start, goal


def loai_vung_cam(h, ke, vung_cam):
    """Tao do thi moi da loai han cac dinh vung cam (ca dinh lan canh noi toi no)."""
    ke_moi = {}
    for ten, ds in ke.items():
        if ten in vung_cam:
            continue
        ke_moi[ten] = [(lg, cp) for (lg, cp) in ds
                       if lg not in vung_cam and lg in h]
    return ke_moi


def a_star(h, ke, start, goal):
    """A* graph-search. Hang doi uu tien theo (f, ten). Tra ve (duong_di, chi_phi) hoac None."""
    if start not in ke or goal not in ke:
        return None

    g = {start: Decimal(0)}
    cha = {start: None}
    dong = set()                       # tap cac dinh da chot
    hang_doi = [(g[start] + h[start], start)]

    while hang_doi:
        f, u = heapq.heappop(hang_doi)
        if u in dong:                  # ban ghi cu, bo qua
            continue
        dong.add(u)

        if u == goal:
            duong = []
            cur = u
            while cur is not None:
                duong.append(cur)
                cur = cha[cur]
            duong.reverse()
            return duong, g[u]

        for v, cp in ke[u]:
            if v in dong:              # dinh da chot khong xu ly lai
                continue
            moi = g[u] + cp
            # chi cap nhat khi chi phi THAP HON NGHIEM NGAT
            if v not in g or moi < g[v]:
                g[v] = moi
                cha[v] = u
                heapq.heappush(hang_doi, (moi + h[v], v))

    return None


def main():
    h, ke, vung_cam, start, goal = doc_du_lieu()

    # Neu xuat phat hoac dich nam trong vung cam thi khong co duong di
    if start in vung_cam or goal in vung_cam:
        print("NO_PATH")
        return

    # Buoc 1: loai bo vung cam TRUOC khi chay A*
    ke_moi = loai_vung_cam(h, ke, vung_cam)

    # Buoc 2: chay A*
    kq = a_star(h, ke_moi, start, goal)

    # Buoc 3: in ket qua
    # Dong 1: cac dinh tren duong di, cach nhau 1 dau cach
    # Dong 2: COST=<tong chi phi cac canh tren duong di>
    # Neu khong co duong di hop le: in NO_PATH
    if kq is None:
        print("NO_PATH")
    else:
        duong, chi_phi = kq
        print(" ".join(duong))
        print("COST=" + dinh_dang_so(chi_phi))


if __name__ == "__main__":
    main()

    ##salam alaykum bitches