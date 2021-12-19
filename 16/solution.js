const net = require("net");
const assert = require("assert");
const _ = require("lodash");
const gcd = require('gcd');
const readlinePromises = require('readline');
const util = require('util');

const DEBUG = true;

const getDivisors = (n) => {
    const divisors = [];
    for (let i = 2; i <= n; i++) {
        if (n % i === 0) {
            divisors.push(i);
        }
    }
    return divisors;
};

const isPrimish = (n) => getDivisors(n).length < 2;

const computePrimishes = (maxNumber) => {
    const primishes = new Set();
    for (let i = 1; i < maxNumber; i++) {
        if (isPrimish(i)) {
            primishes.add(i);
        }
    }
    return primishes;
};

const createJudgeClient = () => {

    const client = new net.Socket();
    client.connect(7162, "codechallenge-daemons.0x14.net", () => { });

    // const killTime = setTimeout(() => {
    //     client.write("bye");
    // }, 3000);

    client.on("close", (data) => {
        console.log("Server closed connection.");
        // clearTimeout(killTime);
        client.destroy();
    });

    const sendReceive = (command) => {
        return new Promise((resolve, _) => {
            const recv = (data) => {
                const response = data.toString("utf8");
                client.off("data", recv);
                resolve(response);
                DEBUG && console.log(" < ", response);
            }
            client.on("data", recv);
            client.write(command);
            DEBUG && console.log(" > ", command);
        });
    }

    const bye = () => {
        client.write("bye");
    }

    const receiveWelcome = () => {
        return new Promise((resolve, _) => {
            const recv = (data) => {
                const response = data.toString("utf8");
                client.off("data", recv);
                const [n, q] = response.split(" ").map(Number);
                resolve([n, q]);
                DEBUG && console.log(" WELCOME < ", response);
            }
            client.on("data", recv);
        });
    }

    const ask = async (pos1, pos2) => {
        const answer = await sendReceive(`? ${pos1 + 1} ${pos2 + 1}`);
        return Number(answer);
    };

    const submitAnswer = async(positions) => {
        const answer = await sendReceive(`! ${positions.map(x => x + 1).join(" ")}`);
        console.log(answer);
    }

    return {
        receiveWelcome,
        ask,
        submitAnswer,
        bye
    };

}

const upto = (n) => {
    const numbers = [];
    for (let i = 1; i <= n; i++) {
        numbers.push(i);
    }
    return numbers;
}

const createFakeJudge = (n, q, givenNumbers) => {

    let queriesLeft = q;
    const numbers = givenNumbers || _.shuffle(upto(n));
    const primishPositions = [];
    numbers.forEach((n, i) => {
        if (isPrimish(n)) {
            primishPositions.push(i);
        }
    });
    console.log(numbers);
    console.log(primishPositions);

    const receiveWelcome = async () => {
        return [n, q];
    }

    const ask = async(pos1, pos2) => {
        checkQueryLimit();
        DEBUG && console.log(`> ask ${pos1} ${pos2}`); //, where numbers ${numbers[pos1]} and ${numbers[pos2]} are.`);
        const x1 = numbers[pos1];
        const x2 = numbers[pos2];
        const ans = gcd(x1, x2);
        DEBUG && console.log(`< ${ans}`);
        return ans;
    }

    const submitAnswer = async(positions) => {
        checkQueryLimit();
        console.log(`> submit ${positions.map(p => p + 1).join(" ")}`);

        if (positions.length !== primishPositions.length) {
            throw new Error(
                `Length not OK (expected ${primishPositions.length} numbers, but got ${positions.length})`);
        }
        for (let i = 0; i < positions.length; i++) {
            if (positions[i] === primishPositions[i]) {
                continue;
            }
            throw new Error(
                `Mismatch at position ${i}: Expected ${primishPositions[i]}, got ${positions[i]}`);
        }
        console.log(`Congrats, you got the SUPERPASSWORD in ${q - queriesLeft} queries!`);
        return true;
    }

    const checkQueryLimit = () => {
        queriesLeft--;
        if (queriesLeft < 0) {
            throw new Error(`${q} queries exceeded.`);
        }
    };

    const bye = () => {
        throw new Error("Disconnected on request.");
    };

    return {
        receiveWelcome,
        ask,
        submitAnswer,
        bye
    }
}

createManualSolver = (judge) => {
    const rl = readlinePromises.createInterface({
    input: process.stdin,
    output: process.stdout
    });

    const question = util.promisify(rl.question).bind(rl);

    const solve = async () => {
        while (true) {
            const command = await question("Enter 2 poss for gcd, or more to submit answer: ");
            const items = command.split(" ").map(Number);
            if (items.length === 2) {
                judge.ask(...items);
            } else {
                const answer = judge.submitAnswer(items);
                if (answer) {
                    rl.close();
                    return;
                }
            }
        }
    };
    return { solve };
};

const createSolver = (judge, n, q) => {

    const numbers = [];
    let positions = [];
    const knownDivisors = {};
    for (let i = 1; i <= n; i++) {
        numbers.push(i);
        positions.push(i - 1);
        knownDivisors[i] = getDivisors(i);
    }

    const primes = numbers.filter(n => n > 1 && isPrimish(n));

    const divisorCounts = {};
    for (const n of numbers) {
        for (const d of knownDivisors[n]) {
            divisorCounts[d] = (divisorCounts[d] ?? 0) + 1;
        }
    }

    const divs = positions.map(_ => new Set());
    const nonDivs = positions.map(_ => new Set());
    const coprimes = {};
    const commonDivisors = {};
    const alreadySeen = {};
    positions.forEach(x => {
        coprimes[x] = new Set();
        commonDivisors[x] = new Set();
        alreadySeen[x] = new Set();
    });
    const expectedPrimeCount = numbers.filter(x => isPrimish(x)).length;
    // true = primish; false = non-primish; undefined = unknown
    const status = numbers.map(_ => undefined);

    const getNewPair = () => {
        const p1s = _.sortBy(
            positions
            .filter(p => status[p] !== true)
            .filter(p => alreadySeen[p].size !== n - 1)
            , p => [
                -divs[p].size,
                status[p] === undefined ? 1 : 0,
            ]
        );
        const unknownPositions = positions.filter(p => status[p] === undefined);

        for (const p1 of p1s) {
            const nextCandidates = unknownPositions.filter(
                p => p != p1 && !alreadySeen[p].has(p1));
            const p2 = _.minBy(nextCandidates, p => [
                status[p] === undefined ? 0 : 1,
                -divs[p].size,
            ]);
            if (p2 === undefined) {
                continue;
            }
            // Avoid queries, when p1 and p2 have at least 2 divs in common.
            const commonDivisors = new Set(
                [...divs[p1]].filter(x => divs[p1].has(x)));

            if (commonDivisors.length > 1) {
                continue;
            }

            return [p1, p2];
        }
    };

    const primesFound = new Set();

    const markPrime = (pos) => {
        status[pos] = true;
        for (const pp of commonDivisors[pos]) {
            DEBUG && console.log(`Marking ${pp} as nonprime, as it is divisible by prime at ${pos}`);
            status[pp] = false;
        }
    };

    const solve = async () => {

        while (true) {

            // Heuristic: identify primes when all their multiples have been found.
            for (const p of primes) {
                if (primesFound.has(p)) {
                    continue;
                }
                let count = 0;
                for (const ds of divs) {
                    if (ds.has(p)) {
                        count++;
                    }
                }
                if (count === divisorCounts[p]) {
                    // all multiples of p found; the one with just p is a prime.
                    const ps = positions.filter(pos => divs[pos].has(p) && divs[pos].size === 1);
                    if (ps.length === 1) {
                        DEBUG && console.log(`Found prime: ${p}`);
                        primesFound.add(p);
                        markPrime(ps[0]);
                    }
                }
            }

            const possiblyPrimeCount = status.filter(s => s !== false).length;
            if (possiblyPrimeCount === expectedPrimeCount) {
                const primishPositions = [];
                status.forEach((s, i) => {
                    if (s !== false) {
                        primishPositions.push(i);
                    }
                });
                judge.submitAnswer(primishPositions);
                return;
            }

            const newPair = getNewPair();

            if (newPair === undefined) {
                // all pairs have been visited!
                // Time to mark all items without divisors as primes
                for (const p of positions) {
                    if (divs[p].size === 0) {
                        markPrime(p);
                    }
                }
                const foundPrimeCount = status.filter(s => s === true).length;
                if (foundPrimeCount === expectedPrimeCount) {
                    continue;
                }

                console.log({
                    divs,
                    nonDivs,
                    status,
                    primes: status.filter(s => s === true).length,
                    nonprimes: status.filter(s => s === false).length,
                    unknown: status.filter(s => s === undefined).length,
                    coprimes,
                    alreadySeen,
                    expectedPrimeCount
                });
                throw new Error("no new pair, and not all primes found.");
            }

            const [p1, p2] = newPair;

            try {
                const gcd = await judge.ask(p1, p2);

                alreadySeen[p1].add(p2);
                alreadySeen[p2].add(p1);

                if (gcd === 1) {
                    coprimes[p1].add(p2);
                    coprimes[p2].add(p1);
                    if (coprimes[p1].size === n - 1) { markPrime[p1]; }
                    if (coprimes[p2].size === n - 1) { markPrime[p2]; }
                    for (const d1 in divs[p1]) { nonDivs[p2].add(d1); }
                    for (const d2 in divs[p2]) { nonDivs[p1].add(d2); }
                } else {
                    commonDivisors[p1].add(p2);
                    commonDivisors[p2].add(p1);
                    const ds = getDivisors(gcd);
                    for (const d of ds) {
                        divs[p1].add(d);
                        divs[p2].add(d);
                    }
                    if (divs[p1].size > 1) { status[p1] = false; }
                    if (divs[p2].size > 1) { status[p2] = false; }
                }
            } catch (e) {
                console.log({
                    // divs,
                    // nonDivs,
                    status,
                    primes: status.filter(s => s === true).length,
                    nonprimes: status.filter(s => s === false).length,
                    unknown: status.filter(s => s === undefined).length,
                    // coprimes,
                    // alreadySeen,
                    expectedPrimeCount
                });
                throw e;
            }

        }
    }

    return { solve };
};

const main = async () => {
    const judge = createJudgeClient();
    // const judge = createFakeJudge(100, 1500);
    const [n, q] = await judge.receiveWelcome();
    const solver = createSolver(judge, n, q);
    // const solver = createManualSolver(judge);
    await solver.solve();
};

main();

