#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

long long int MOD = 100000007;

bool isTuentistic(long long int n) {
    string s = to_string(n);
    for (int pos = s.length() - 2; pos >= 0; pos -= 3) {
        if (s[pos] == '2') {
            return true;
        }
    }
    return false;
}

long long compute(long long n) {
    long long p = 1;
    for (long long i = 1; i <= n; i++) {
        if (!isTuentistic(i)) {
            p *= i;
            p %= MOD;
        }
    }
    return p;
}

vector<long long> precomputeAll() {
    vector<long long int> result;
    long long int p = 1;
    for (long long i = 1; i < MOD; i++) {
        if (!isTuentistic(i)) {
            p *= i;
            p %= MOD;
        }
        result.push_back(p);
    }

    return result;
}

int main() {

    vector<long long int> answers = precomputeAll();

    int t;
    cin >> t;
    for (int i = 0; i < t; i++) {
        string ns;
        cin >> ns;
        long long result = 0;
        long long n = 0;
        if (ns.length() < 10) {
            n = stoll(ns);
            if (n < MOD) {
                result = answers[n-1];
            }
        }

        cout << "Case #" << i + 1 << ": " << result << endl;

    }

    return 0;
}
