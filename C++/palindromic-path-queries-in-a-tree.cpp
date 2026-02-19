// Time:  O((n + q) * logn)
// Space: O(nlogn)

// dfs, lca, binary lifting, fenwick tree
class Solution {
public:
    vector<bool> palindromePath(int n, vector<vector<int>>& edges, string s, vector<string>& queries) {
        vector<int> prefix(n);
        const auto& callback = [&](int u, int p) {
            prefix[u] = (p != -1 ? prefix[p] : 0) ^ ( 1<< (s[u] - 'a'));
        };

        vector<vector<int>> adj(n);
        for (const auto& e : edges) {
            adj[e[0]].emplace_back(e[1]);
            adj[e[1]].emplace_back(e[0]);
        }
        TreeInfos tree_infos(adj, callback);
        BIT bit(n + 1);
        vector<bool> result;
        for (const auto& q : queries) {
            stringstream ss(q);
            string op;
            int u;
            ss >> op >> u;
            if (op == "update") {
                char c;
                ss >> c;
                const auto& diff = (1 << (s[u] - 'a')) ^ (1 << (c - 'a'));
                if (!diff) {
                    continue;
                }
                s[u] = c;
                bit.add(tree_infos.left(u), diff);
                bit.add(tree_infos.right(u) + 1, diff);
            } else {
                int v;
                ss >> v;
                const auto& l = tree_infos.lca(u, v);
                const auto& val = (prefix[u] ^ bit.query(tree_infos.left(u))) ^ (prefix[v] ^ bit.query(tree_infos.left(v))) ^ (1 << (s[l] - 'a'));
                result.emplace_back((val & (val - 1)) == 0);
            }
        }
        return result;
    }

private:
    class BIT {
    public:
        BIT(int n) : bit_(n + 1) {  // 0-indexed
        }
        
        void add(int i, int val) {
            ++i;
            for (; i < size(bit_); i += lower_bit(i)) {
                bit_[i] ^= val;
            }
        }

        int query(int i) const {
            ++i;
            int total = 0;
            for (; i > 0; i -= lower_bit(i)) {
                total ^= bit_[i];
            }
            return total;
        }

    private:
        inline int lower_bit(int i) const {
            return i & -i;
        }
        
        vector<int> bit_;
    };

    class TreeInfos {
    public:
        TreeInfos(const vector<vector<int>>& adj, const auto& cb)  // modified
         : L_(size(adj))
         , R_(size(adj))
         , D_(size(adj))
         , P_(size(adj)) {

             const int N = size(adj);
             int idx = -1;
             vector<tuple<int, int, int>> stk = {{1, 0, -1}};
             while (!empty(stk)) {
                const auto [step, u, p] = stk.back(); stk.pop_back();
                if (step == 1) {
                    cb(u, p);  // added
                    D_[u] = (p == -1) ? 1 : D_[p] + 1;
                    if (p != -1) {
                        P_[u].emplace_back(p);  // ancestors of the node i
                    }
                    for (int i = 0; i < size(P_[u]); ++i) {
                        if (i >= size(P_[P_[u][i]])) {
                            break;
                        }
                        P_[u].emplace_back(P_[P_[u][i]][i]);
                    }
                    L_[u] = ++idx; 
                    stk.emplace_back(2, u, -1);
                    for (int i = size(adj[u]) -1; i >= 0; --i) {
                        const auto& v = adj[u][i];
                        if (v == p) {
                            continue;
                        }
                        stk.emplace_back(1, v, u);
                    }
                } else if (step == 2) {
                    R_[u] = idx;
                }
            }
            assert(idx == N - 1);
        }
        
        bool is_ancestor(int a, int b) const {
            return L_[a] <= L_[b] && R_[b] <= R_[a];
        }

        int lca(int a, int b) const {
            if (D_[a] > D_[b]) {
                swap(a, b);
            }
            if (is_ancestor(a, b)) {
                return a;
            }
            for (int i = size(P_[a]) - 1; i >= 0; --i) {  // O(logN)
                if (i < size(P_[a]) && !is_ancestor(P_[a][i], b)) {
                    a = P_[a][i];
                }
            }
            return P_[a][0];
        }

        int left(int a) const {
            return L_[a];
        }

        int right(int a) const {
            return R_[a];
        }
        
        int depth(int a) const {
            return D_[a];
        }
    
    private:
        vector<int> L_;
        vector<int> R_;
        vector<int> D_;
        vector<vector<int>> P_;
    };
};

// Time:  O((n + q) * logn)
// Space: O(nlogn)
// dfs, lca, binary lifting, fenwick tree
class Solution2 {
public:
    vector<bool> palindromePath(int n, vector<vector<int>>& edges, string s, vector<string>& queries) {
        vector<vector<int>> adj(n);
        for (const auto& e : edges) {
            adj[e[0]].emplace_back(e[1]);
            adj[e[1]].emplace_back(e[0]);
        }
        TreeInfos tree_infos(adj);
        BIT bit(n + 1);
        for (int u = 0; u < n; ++u) {
            const auto& diff = 1 << (s[u] - 'a');
            bit.add(tree_infos.left(u), diff);
            bit.add(tree_infos.right(u) + 1, diff);
        }
        vector<bool> result;
        for (const auto& q : queries) {
            stringstream ss(q);
            string op;
            int u;
            ss >> op >> u;
            if (op == "update") {
                char c;
                ss >> c;
                const auto& diff = (1 << (s[u] - 'a')) ^ (1 << (c - 'a'));
                if (!diff) {
                    continue;
                }
                s[u] = c;
                bit.add(tree_infos.left(u), diff);
                bit.add(tree_infos.right(u) + 1, diff);
            } else {
                int v;
                ss >> v;
                const auto& l = tree_infos.lca(u, v);
                const auto& val = bit.query(tree_infos.left(u)) ^ bit.query(tree_infos.left(v)) ^ (1 << (s[l] - 'a'));
                result.emplace_back(val == 0 || (val & (val - 1)) == 0);
            }
        }
        return result;
    }

private:
    class BIT {
    public:
        BIT(int n) : bit_(n + 1) {  // 0-indexed
        }
        
        void add(int i, int val) {
            ++i;
            for (; i < size(bit_); i += lower_bit(i)) {
                bit_[i] ^= val;
            }
        }

        int query(int i) const {
            ++i;
            int total = 0;
            for (; i > 0; i -= lower_bit(i)) {
                total ^= bit_[i];
            }
            return total;
        }

    private:
        inline int lower_bit(int i) const {
            return i & -i;
        }
        
        vector<int> bit_;
    };

    class TreeInfos {
    public:
        TreeInfos(const vector<vector<int>>& adj)
         : L_(size(adj))
         , R_(size(adj))
         , D_(size(adj))
         , P_(size(adj)) {

             const int N = size(adj);
             int idx = -1;
             vector<tuple<int, int, int>> stk = {{1, 0, -1}};
             while (!empty(stk)) {
                const auto [step, u, p] = stk.back(); stk.pop_back();
                if (step == 1) {
                    D_[u] = (p == -1) ? 1 : D_[p] + 1;
                    if (p != -1) {
                        P_[u].emplace_back(p);  // ancestors of the node i
                    }
                    for (int i = 0; i < size(P_[u]); ++i) {
                        if (i >= size(P_[P_[u][i]])) {
                            break;
                        }
                        P_[u].emplace_back(P_[P_[u][i]][i]);
                    }
                    L_[u] = ++idx; 
                    stk.emplace_back(2, u, -1);
                    for (int i = size(adj[u]) -1; i >= 0; --i) {
                        const auto& v = adj[u][i];
                        if (v == p) {
                            continue;
                        }
                        stk.emplace_back(1, v, u);
                    }
                } else if (step == 2) {
                    R_[u] = idx;
                }
            }
            assert(idx == N - 1);
        }
        
        bool is_ancestor(int a, int b) const {
            return L_[a] <= L_[b] && R_[b] <= R_[a];
        }

        int lca(int a, int b) const {
            if (D_[a] > D_[b]) {
                swap(a, b);
            }
            if (is_ancestor(a, b)) {
                return a;
            }
            for (int i = size(P_[a]) - 1; i >= 0; --i) {  // O(logN)
                if (i < size(P_[a]) && !is_ancestor(P_[a][i], b)) {
                    a = P_[a][i];
                }
            }
            return P_[a][0];
        }

        int left(int a) const {
            return L_[a];
        }

        int right(int a) const {
            return R_[a];
        }
        
        int depth(int a) const {
            return D_[a];
        }
    
    private:
        vector<int> L_;
        vector<int> R_;
        vector<int> D_;
        vector<vector<int>> P_;
    };
};
