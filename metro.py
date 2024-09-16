from collections import deque
import math
import sys

class GraphM:
    class Vertex:
        def __init__(self, name):
            self.name = name
            self.nbrs = {}

    def __init__(self):
        self.vtces = {}

    def add_vertex(self, name):
        if name not in self.vtces:
            self.vtces[name] = self.Vertex(name)

    def add_edge(self, vname1, vname2, dist):
        if vname1 in self.vtces and vname2 in self.vtces:
            self.vtces[vname1].nbrs[vname2] = dist
            self.vtces[vname2].nbrs[vname1] = dist

    def contains_vertex(self, vname):
        return vname in self.vtces

    def contains_edge(self, vname1, vname2):
        return vname1 in self.vtces and vname2 in self.vtces[vname1].nbrs

    def num_vertex(self):
        return len(self.vtces)

    def num_edges(self):
        count = 0
        for _, vtx in self.vtces.items():
            count += len(vtx.nbrs)
        return count // 2

    def display_map(self):
        print("\n***********************************************************************\n")
        for _, vtx in self.vtces.items():
            print(f"{vtx.name} ==> ", end="")
            for nbr, dist in vtx.nbrs.items():
                print(f"{nbr}({dist})", end=" ")
            print()
        print("\n***********************************************************************\n")

    def display_stations(self):
        print("\n***********************************************************************\n")
        i = 1
        for key in self.vtces:
            print(f"{i}. {key}")
            i += 1
        print("\n***********************************************************************\n")
    def get_stations(self):
        return list(self.vtces.keys())


    def has_path(self, vname1, vname2, processed):
        if self.contains_edge(vname1, vname2):
            return True

        processed[vname1] = True
        vtx = self.vtces.get(vname1)
        if not vtx:
            return False

        for nbr in vtx.nbrs:
            if nbr not in processed:
                if self.has_path(nbr, vname2, processed):
                    return True

        return False

    class DijkstraPair:
        def __init__(self, vname, psf, cost):
            self.vname = vname
            self.psf = psf
            self.cost = cost

        def __lt__(self, other):
            return self.cost < other.cost

    def dijkstra(self, src, des, nan):
        print(f"Dijkstra called with src: {src}, des: {des}, nan: {nan}")
        val = 0
        ans = []
        map = {}
        heap = []

        for key in self.vtces:
            np = self.DijkstraPair(key, "", float('inf'))
            if key == src:
                np.cost = 0
                np.psf = key
            heap.append(np)
            map[key] = np

        heap.sort()

        while heap:
            rp = heap.pop(0)

            if rp.vname == des:
                val = rp.cost
                break

            map.pop(rp.vname, None)
            ans.append(rp.vname)

            v = self.vtces[rp.vname]
            for nbr in v.nbrs:
                if nbr in map :
                    if self.is_same_line(rp.vname) == self.is_same_line(nbr) or 'BG' in nbr:
                        oc = map[nbr].cost
                        k = self.vtces[rp.vname]
                        nc = rp.cost + (120 + 40 * k.nbrs[nbr] if nan else k.nbrs[nbr])

                    if nc < oc:
                        gp = map[nbr]
                        #gp.psf = rp.psf + nbr#
                        gp.psf = rp.psf + " ==> " + nbr if 'BG' in nbr else rp.psf + " -> " + nbr
                        gp.cost = nc
                        heap.sort()
        print(f"Dijkstra result: {val}") 
        return val


    class Pair:
        def __init__(self, vname, psf, min_dis, min_time):
            self.vname = vname
            self.psf = psf
            self.min_dis = min_dis
            self.min_time = min_time

    def get_minimum_distance(self, src, dst):
        min_dis = float('inf')
        ans = ""
        processed = {}
        stack = deque()

        sp = self.Pair(src, src + "  ", 0, 0)
        stack.appendleft(sp)

        while stack:
            rp = stack.popleft()

            if rp.vname in processed:
                continue

            processed[rp.vname] = True

            if rp.vname == dst:
                if rp.min_dis < min_dis:
                    ans = rp.psf
                    min_dis = rp.min_dis
                continue

            rpvtx = self.vtces[rp.vname]
            for nbr in rpvtx.nbrs:
                if nbr not in processed:
                    #np = self.Pair(nbr, rp.psf + nbr + "  ", rp.min_dis + rpvtx.nbrs[nbr], 0)#
                    np = self.Pair(nbr, rp.psf + " ==> " + nbr if 'BG' in nbr else rp.psf + " -> " + nbr, rp.min_dis + rpvtx.nbrs[nbr], 0)
                    stack.appendleft(np)

        ans += str(min_dis)
        return ans
    
    def get_minimum_distance(self, src, dst):
        min_dis = float('inf')
        ans =""
        processed = {}
        stack = deque()

        sp = self.Pair(src, src + "  ", 0, 0)
        stack.appendleft(sp)

        while stack:
            rp = stack.popleft()

            if rp.vname in processed:
                continue

            processed[rp.vname] = True

            if rp.vname == dst:
                if rp.min_dis < min_dis:
                    ans = rp.psf
                    min_dis = rp.min_dis
                continue

            rpvtx = self.vtces[rp.vname]
            for nbr in rpvtx.nbrs:
                if nbr not in processed:
                    np = self.Pair(nbr, rp.psf + " ==> " + nbr if 'BG' in nbr else rp.psf + " -> " + nbr, rp.min_dis + rpvtx.nbrs[nbr], 0)
                    stack.appendleft(np)

    # Remove trailing spaces and add the minimum distance
        ans = ans.strip() + " " + str(min_dis)
        return ans


    def get_minimum_time(self, src, dst):
        min_time = float('inf')
        ans = ""
        processed = {}
        stack = deque()

        sp = self.Pair(src, src + "  ", 0, 0)
        stack.appendleft(sp)

        while stack:
            rp = stack.popleft()

            if rp.vname in processed:
                continue

            processed[rp.vname] = True

            if rp.vname == dst:
                if rp.min_time < min_time:
                    ans = rp.psf
                    min_time = rp.min_time
                continue

            rpvtx = self.vtces[rp.vname]
            for nbr in rpvtx.nbrs:
                if nbr not in processed:
                    np = self.Pair(nbr, rp.psf + nbr + "  ", 0, rp.min_time + 120 + 40 * rpvtx.nbrs[nbr])
                    stack.appendleft(np)

        minutes = math.ceil(min_time / 60)
        ans += str(minutes)
        return ans

    def get_interchanges(self, str_path):
        arr = []
        res = str_path.split("  ")
        arr.append(res[0])
        count = 0
        for i in range(1, len(res) - 1):
            index = res[i].find('~')
            s = res[i][index + 1:]

            if len(s) == 2:
                prev = res[i - 1][res[i - 1].find('~') + 1:]
                next = res[i + 1][res[i + 1].find('~') + 1:]

                if prev == next:
                    arr.append(res[i])
                else:
                    arr.append(res[i] + " ==> " + res[i + 1])
                    i += 1
                    count += 1
            else:
                arr.append(res[i])

        arr.append(str(count))
        arr.append(res[-1])
        return arr


    def create_metro_map(self):
        # Blue Line
        self.add_vertex("Wimco Nagar Depot~B")
        self.add_vertex("Wimco Nagar~B")
        self.add_vertex("Thiruvottriyur~B")
        self.add_vertex("Thiruvottriyur Theradi~B")
        self.add_vertex("Kaladipet~B")
        self.add_vertex("Tollgate~B")
        self.add_vertex("New Washermanpet~B")
        self.add_vertex("Tondiarpet~B")
        self.add_vertex("Sir Theagaraya College~B")
        self.add_vertex("Washermanpet~B")
        self.add_vertex("Mannadi~B")
        self.add_vertex("High Court~B")
        self.add_vertex("MGR Central (Chennai Central)~BG")  # Interchange station
        self.add_vertex("Government Estate~B")
        self.add_vertex("LIC~B")
        self.add_vertex("Thousand Lights~B")
        self.add_vertex("AG DMS~B")
        self.add_vertex("Teynampet~B")
        self.add_vertex("Nandanam~B")
        self.add_vertex("Saidapet~B")
        self.add_vertex("Little Mount~B")
        self.add_vertex("Guindy~B")
        self.add_vertex("Arignar Anna Alandur~BG")  # Interchange station
        self.add_vertex("Nanganallur Road~B")
        self.add_vertex("Meenambakkam~B")
        self.add_vertex("Chennai International Airport~B")
        # Green Line
        self.add_vertex("Egmore~G")
        self.add_vertex("Nehru Park~G")
        self.add_vertex("Kilpauk Medical College~G")
        self.add_vertex("Pachaiyappa College~G")
        self.add_vertex("Shenoy Nagar~G")
        self.add_vertex("Anna Nagar East~G")
        self.add_vertex("Anna Nagar Tower~G")
        self.add_vertex("Thirumangalam~G")
        self.add_vertex("Koyambedu~G")
        self.add_vertex("CMBT~G")
        self.add_vertex("Arumbakkam~G")
        self.add_vertex("Vadapalani~G")
        self.add_vertex("Ashok Nagar~G")
        self.add_vertex("Ekkattuthangal~G")
        self.add_vertex("St Thomas Mount~G")

        # Blue Line Edges
        self.add_edge("Wimco Nagar Depot~B", "Wimco Nagar~B", 1)
        self.add_edge("Wimco Nagar~B", "Thiruvottriyur~B", 2)
        self.add_edge("Thiruvottriyur~B", "Thiruvottriyur Theradi~B", 1)
        self.add_edge("Thiruvottriyur Theradi~B", "Kaladipet~B", 1)
        self.add_edge("Kaladipet~B", "Tollgate~B", 1)
        self.add_edge("Tollgate~B", "New Washermanpet~B", 2)
        self.add_edge("New Washermanpet~B", "Tondiarpet~B", 1)
        self.add_edge("Tondiarpet~B", "Sir Theagaraya College~B", 1)
        self.add_edge("Sir Theagaraya College~B", "Washermanpet~B", 1)
        self.add_edge("Washermanpet~B", "Mannadi~B", 1)
        self.add_edge("Mannadi~B", "High Court~B", 1)
        self.add_edge("High Court~B", "MGR Central (Chennai Central)~BG", 2)
        self.add_edge("MGR Central (Chennai Central)~BG", "Government Estate~B", 1)
        self.add_edge("Government Estate~B", "LIC~B", 1)
        self.add_edge("LIC~B", "Thousand Lights~B", 1)
        self.add_edge("Thousand Lights~B", "AG DMS~B", 1)
        self.add_edge("AG DMS~B", "Teynampet~B", 1)
        self.add_edge("Teynampet~B", "Nandanam~B", 1)
        self.add_edge("Nandanam~B", "Saidapet~B", 1)
        self.add_edge("Saidapet~B", "Little Mount~B", 1)
        self.add_edge("Little Mount~B", "Guindy~B", 1)
        self.add_edge("Guindy~B", "Arignar Anna Alandur~BG", 2)
        self.add_edge("Arignar Anna Alandur~BG", "Nanganallur Road~B", 1)
        self.add_edge("Nanganallur Road~B", "Meenambakkam~B", 1)
        self.add_edge("Meenambakkam~B", "Chennai International Airport~B", 2)

        # Green Line Edges
        self.add_edge("MGR Central (Chennai Central)~BG", "Egmore~G", 1)
        self.add_edge("Egmore~G", "Nehru Park~G", 1)
        self.add_edge("Nehru Park~G", "Kilpauk Medical College~G", 1)
        self.add_edge("Kilpauk Medical College~G", "Pachaiyappa College~G", 1)
        self.add_edge("Pachaiyappa College~G", "Shenoy Nagar~G", 1)
        self.add_edge("Shenoy Nagar~G", "Anna Nagar East~G", 1)
        self.add_edge("Anna Nagar East~G", "Anna Nagar Tower~G", 1)
        self.add_edge("Anna Nagar Tower~G", "Thirumangalam~G", 1)
        self.add_edge("Thirumangalam~G", "Koyambedu~G", 1)
        self.add_edge("Koyambedu~G", "CMBT~G", 1)
        self.add_edge("CMBT~G", "Arumbakkam~G", 1)
        self.add_edge("Arumbakkam~G", "Vadapalani~G", 1)
        self.add_edge("Vadapalani~G", "Ashok Nagar~G", 1)
        self.add_edge("Ashok Nagar~G", "Ekkattuthangal~G", 1)
        self.add_edge("Ekkattuthangal~G", "Arignar Anna Alandur~BG", 2)
        self.add_edge("Arignar Anna Alandur~BG", "St Thomas Mount~G", 1)

    
    blue_line_stations = [
        "Wimco Nagar Depot~B", "Wimco Nagar~B", "Thiruvottriyur~B", "Thiruvottriyur Theradi~B", "Kaladipet~B", "Tollgate~B",
        "New Washermanpet~B", "Tondiarpet~B", "Sir Theagaraya College~B", "Washermanpet~B", "Mannadi~B", "High Court~B",
        "MGR Central (Chennai Central)~BG", "Government Estate~B", "LIC~B", "Thousand Lights~B", "AG DMS~B", "Teynampet~B",
        "Nandanam~B", "Saidapet~B", "Little Mount~B", "Guindy~B", "Arignar Anna Alandur~BG", "Nanganallur Road~B", "Meenambakkam~B", "Chennai International Airport~B"
    ]

    green_line_stations = [
        "MGR Central (Chennai Central)~BG", "Egmore~G", "Nehru Park~G", "Kilpauk Medical College~G", "Pachaiyappa College~G", "Shenoy Nagar~G", "Anna Nagar East~G",
        "Anna Nagar Tower~G", "Thirumangalam~G", "Koyambedu~G", "CMBT~G", "Arumbakkam~G", "Vadapalani~G", "Ashok Nagar~G", "Ekkattuthangal~G", 
        "Arignar Anna Alandur~BG", "St Thomas Mount~G"
    ]

    @staticmethod
    def is_same_line(station):
        if station in GraphM.blue_line_stations or station.endswith('~B'):
            return 'blue'
        elif station in GraphM.green_line_stations or station.endswith('~G'):
            return 'green'
        elif station.endswith('~BG'):
            return 'both'
        return 'unknown'

    @staticmethod
    def print_code_list(self):
        print("List of stations along with their codes:\n")
        keys = list(self.vtces.keys())
        codes = {}
        for i, key in enumerate(keys, start=1):
            # Generate a unique code based on the first letter of each word and the line
            words = key.split()
            code = ''.join(word[0].upper() for word in words if word[0].isalpha())
            line = key[-1]  # Get the line (B or G)
            code += line
            
            # If code already exists, append a number
            base_code = code
            suffix = 1
            while code in codes.values():
                code = f"{base_code}{suffix}"
                suffix += 1
            
            codes[key] = code
            
            print(f"{i}. {key}\t", end="")
            if len(key) < 22:
                print("\t", end="")
            if len(key) < 14:
                print("\t", end="")
            if len(key) < 6:
                print("\t", end="")
            print(code)
        
        return codes

    @staticmethod
    def main():
        g = GraphM()
        GraphM.create_metro_map(g)

        print("\n\t\t\t****WELCOME TO THE METRO APP*****")

        while True:
            print("\t\t\t\t~~LIST OF ACTIONS~~\n\n")
            print("1. LIST ALL THE STATIONS IN THE MAP")
            print("2. SHOW THE METRO MAP")
            print("3. GET SHORTEST DISTANCE FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
            print("4. GET SHORTEST TIME TO REACH FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
            print("5. GET SHORTEST PATH (DISTANCE WISE) TO REACH FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
            print("6. GET SHORTEST PATH (TIME WISE) TO REACH FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
            print("7. EXIT THE MENU")
            choice = -1
            try:
                choice = int(input("\nENTER YOUR CHOICE FROM THE ABOVE LIST (1 to 7) : "))
            except Exception:
                pass
            print("\n***********************************************************\n")
            if choice == 7:
                sys.exit(0)

            if choice == 1:
                g.display_stations()
            elif choice == 2:
                g.display_map()
            elif choice == 3:
                codes = GraphM.print_code_list(g)
                print("\n1. TO ENTER SERIAL NO. OF STATIONS\n2. TO ENTER CODE OF STATIONS\n3. TO ENTER NAME OF STATIONS\n")
                ch = int(input("ENTER YOUR CHOICE: "))
                st1 = ""
                st2 = ""
                print("ENTER THE SOURCE AND DESTINATION STATIONS")
                if ch == 1:
                    keys = list(g.vtces.keys())
                    st1 = keys[int(input()) - 1].strip()
                    st2 = keys[int(input()) - 1].strip()
                elif ch == 2:
                    a = input().strip().upper()
                    b = input().strip().upper()
                    st1 = next((station for station, code in codes.items() if code == a), None)
                    st2 = next((station for station, code in codes.items() if code == b), None)
                    if st1 is None or st2 is None:
                        print("Invalid station code(s)")
                        continue
                elif ch == 3:
                    st1 = input().strip()
                    st2 = input().strip()
                else:
                    print("Invalid choice")
                    continue

                print(f"Source Station: {st1}")
                print(f"Destination Station: {st2}")

                processed = {}
                if not g.contains_vertex(st1):
                    print(f"Source station '{st1}' does not exist in the graph.")
                if not g.contains_vertex(st2):
                    print(f"Destination station '{st2}' does not exist in the graph.")
                
                if not g.contains_vertex(st1) or not g.contains_vertex(st2):
                    print("THE INPUTS ARE INVALID")
                elif not g.has_path(st1, st2, processed):
                    print(f"No path exists between '{st1}' and '{st2}'.")
                    print("THE INPUTS ARE INVALID")
                else:
                    distance = g.dijkstra(st1, st2, False)
                    print(f"SHORTEST DISTANCE FROM {st1} TO {st2} IS {distance}KM\n")
                    
                    # Display the path
                    path = g.get_minimum_distance(st1, st2)
                    print("Path:", path)
            elif choice == 4:
                sat1 = input("ENTER THE SOURCE STATION: ").strip()
                sat2 = input("ENTER THE DESTINATION STATION: ").strip()

                processed1 = {}
                if not g.contains_vertex(sat1) or not g.contains_vertex(sat2):
                    print("THE INPUTS ARE INVALID")
                else:
                    print(f"SHORTEST TIME FROM ({sat1}) TO ({sat2}) IS {g.dijkstra(sat1, sat2, True) // 60} MINUTES\n\n")
            elif choice == 5:
                print("ENTER THE SOURCE AND DESTINATION STATIONS")
                s1 = input().strip()
                s2 = input().strip()

                processed2 = {}
                if not g.contains_vertex(s1) or not g.contains_vertex(s2) or not g.has_path(s1, s2, processed2):
                    print("THE INPUTS ARE INVALID")
                else:
                    str_path = g.get_interchanges(g.get_minimum_distance(s1, s2))
                    print("SHORTEST PATH (DISTANCE WISE):", " ==> ".join(str_path))
            elif choice == 6:
                print("ENTER THE SOURCE AND DESTINATION STATIONS")
                s1 = input().strip()
                s2 = input().strip()

                processed2 = {}
                if not g.contains_vertex(s1) or not g.contains_vertex(s2) or not g.has_path(s1, s2, processed2):
                    print("THE INPUTS ARE INVALID")
                else:
                    str_path = g.get_interchanges(g.get_minimum_time(s1, s2))
                    print("SHORTEST PATH (TIME WISE):", " ==> ".join(str_path))

class Heap:
    def __init__(self):
        self.data = []
        self.map = {}

    def add(self, item):
        self.data.append(item)
        self.map[item] = len(self.data) - 1
        self.upheapify(len(self.data) - 1)

    def upheapify(self, ci):
        pi = (ci - 1) // 2
        if self.is_larger(self.data[ci], self.data[pi]) > 0:
            self.swap(pi, ci)
            self.upheapify(pi)

    def swap(self, i, j):
        ith = self.data[i]
        jth = self.data[j]

        self.data[i], self.data[j] = jth, ith
        self.map[ith] = j
        self.map[jth] = i

    def display(self):
        print(self.data)

    def size(self):
        return len(self.data)

    def is_empty(self):
        return self.size() == 0

    def remove(self):
        self.swap(0, len(self.data) - 1)
        rv = self.data.pop()
        self.downheapify(0)

        del self.map[rv]
        return rv

    def downheapify(self, pi):
        lci = 2 * pi + 1
        rci = 2 * pi + 2
        mini = pi

        if lci < len(self.data) and self.is_larger(self.data[lci], self.data[mini]) > 0:
            mini = lci

        if rci < len(self.data) and self.is_larger(self.data[rci], self.data[mini]) > 0:
            mini = rci

        if mini != pi:
            self.swap(mini, pi)
            self.downheapify(mini)

    def get(self):
        return self.data[0]

    def is_larger(self, t, o):
        return (t > o) - (t < o)  # Equivalent to t.compareTo(o) in Java

    def update_priority(self, pair):
        index = self.map[pair]
        self.upheapify(index)

