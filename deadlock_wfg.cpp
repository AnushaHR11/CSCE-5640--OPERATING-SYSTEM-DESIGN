#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm>

using namespace std;

static bool dfsCycle(int u,
                     const vector<vector<int>>& adj,
                     vector<int>& state,          // 0=unvisited,1=visiting,2=done
                     vector<int>& parent,
                     vector<int>& cycleOut) {
    state[u] = 1; // visiting

    for (int v : adj[u]) {
        if (state[v] == 0) {
            parent[v] = u;
            if (dfsCycle(v, adj, state, parent, cycleOut)) return true;
        } else if (state[v] == 1) {
            // Found a back edge u -> v, cycle exists.
            // Reconstruct cycle from u back to v using parent[]
            vector<int> cycle;
            cycle.push_back(v);
            int cur = u;
            while (cur != -1 && cur != v) {
                cycle.push_back(cur);
                cur = parent[cur];
            }
            cycle.push_back(v); // close the loop
            reverse(cycle.begin(), cycle.end());
            cycleOut = cycle;
            return true;
        }
    }

    state[u] = 2; // done
    return false;
}

static bool detectDeadlock(int n, const vector<vector<int>>& adj, vector<int>& cycleOut) {
    vector<int> state(n, 0);
    vector<int> parent(n, -1);

    for (int i = 0; i < n; i++) {
        if (state[i] == 0) {
            if (dfsCycle(i, adj, state, parent, cycleOut)) return true;
        }
    }
    return false;
}

static bool readFromStream(istream& in, int& n, int& m, vector<vector<int>>& adj) {
    if (!(in >> n >> m)) return false;
    if (n <= 0 || m < 0) return false;

    adj.assign(n, {});
    for (int i = 0; i < m; i++) {
        int u, v;
        if (!(in >> u >> v)) return false;
        if (u < 0 || u >= n || v < 0 || v >= n) return false;
        adj[u].push_back(v);
    }
    return true;
}

int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    vector<vector<int>> adj;

    // Parameter passing method:
    // 1) Interactive input (default)
    // 2) File input: ./deadlock_wfg --file input.txt
    if (argc == 3 && string(argv[1]) == "--file") {
        ifstream fin(argv[2]);
        if (!fin) {
            cerr << "Error: Cannot open file.\n";
            return 1;
        }
        if (!readFromStream(fin, n, m, adj)) {
            cerr << "Error: Invalid file format.\n";
            return 1;
        }
    } else {
        cout << "Enter number of processes: ";
        cin >> n;
        cout << "Enter number of edges: ";
        cin >> m;

        if (n <= 0 || m < 0) {
            cout << "Invalid input.\n";
            return 1;
        }

        adj.assign(n, {});
        cout << "Enter edges (u v) meaning: u waits for v\n";
        for (int i = 0; i < m; i++) {
            int u, v;
            cin >> u >> v;
            if (u < 0 || u >= n || v < 0 || v >= n) {
                cout << "Invalid edge.\n";
                return 1;
            }
            adj[u].push_back(v);
        }
    }

    vector<int> cycle;
    bool deadlock = detectDeadlock(n, adj, cycle);

    if (!deadlock) {
        cout << "Deadlock: NO\n";
        cout << "No cycle found in the wait-for graph.\n";
    } else {
        cout << "Deadlock: YES\n";
        cout << "Processes in cycle: ";
        // cycle is like: P2 -> P3 -> P1 -> P2 (first == last)
        for (size_t i = 0; i < cycle.size(); i++) {
            cout << "P" << cycle[i];
            if (i + 1 < cycle.size()) cout << " -> ";
        }
        cout << "\n";
    }

    return 0;
}
