const net = require("net");
const assert = require("assert");

const DEBUG = true;

const DIRECTIONS = {
    north: [0, 1],
    west: [1, 0],
    south: [0, -1],
    east: [-1, 0],
};

const move = ({x, y}, directon) => {
    const [xo, yo] = DIRECTIONS[directon];
    return {
        x: x + xo,
        y: y + yo
    };
};

assert(move({x: 3, y: 4}, "north").x === 3);
assert(move({x: 3, y: 4}, "north").y === 5);
assert(move({x: 3, y: 4}, "west").x === 4);
assert(move({x: 3, y: 4}, "west").y === 4);
assert(move({x: 3, y: 4}, "south").x === 3);
assert(move({x: 3, y: 4}, "south").y === 3);
assert(move({x: 3, y: 4}, "east").x === 2);
assert(move({x: 3, y: 4}, "east").y === 4);

const createMazeClient = (client) => {

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

    const fail = (errorMessage) => {
        bye();
        console.error("FAIL: " + errorMessage);
    };

    const receiveWelcome = () => {
        return new Promise((resolve, _) => {
            const recv = (data) => {
                const response = data.toString("utf8");
                client.off("data", recv);
                resolve(response);
                DEBUG && console.log(" WELCOME < ", response);
            }
            client.on("data", recv);
        });
    }

    const parsePosition = (str) => {
        const match = str.match(/\((\d+), (\d+)\)/);
        if (match === null) {
            fail(`Location not understood: ${str}`);
        }
        return {
            x: Number(match[1]),
            y: Number(match[2])
        };
    };

    const whereAmI = async () => {
        const answer = await sendReceive("where am I");
        return parsePosition(answer);
    };

    const isExit = async () => {
        const answer = await sendReceive("is exit?");
        return answer !== "No. Sorry, traveller...\n";
    };

    const go = async (direction) => {
        const answer = await sendReceive(direction);
        if (!answer.startsWith("Great")) {
            fail(`Go command gone wrong: ${answer}`)
        }
        return parsePosition(answer);
    }

    const goTo = async (coords) => {
        const {x, y} = coords;
        const answer = await sendReceive(`go to ${x},${y}`);
        if (!answer.startsWith("Great")) {
            fail(`Go command gone wrong: ${answer}`)
        }
        return parsePosition(answer);
    }

    const look = async () => {
        const answer = await sendReceive("look");
        const match = answer.trim().match(/movements: (.+)$/);
        if (!match) {
            fail(`Look command gone wrong: ${answer}`);
        }
        return new Set(match[1].split(" "));
    }

    return {
        receiveWelcome,
        whereAmI,
        isExit,
        go,
        goTo,
        look,
        bye
    };

}

class Queue {
    constructor() {
        this.front = [];
        this.back = [];
    }

    get length() {
        return this.front.length + this.back.length;
    }

    enqueue(thing) {
        this.back.push(thing);
    }

    dequeue() {
        if (this.front.length === 0) {
            while(this.back.length > 0) {
                this.front.push(this.back.pop());
            }
        }
        if (this.front.length === 0) {
            throw new Error("Queue empty!");
        }
        return this.front.pop();
    }
}

const q = new Queue();
q.enqueue(1);
q.enqueue(2);
q.enqueue(3);
assert(q.length === 3);
assert(q.dequeue() === 1);
assert(q.dequeue() === 2);
q.enqueue(4);
assert(q.length === 2);
assert(q.dequeue() === 3);
assert(q.dequeue() === 4);
assert(q.length === 0);

const createSolver = (maze) => {

    const shortestFrom = new Map();

    const key = (coords) => `${coords.x},${coords.y}`;

    const markShortestFrom = (to, from) => shortestFrom.set(key(to), from);
    const beenThere = (there) => shortestFrom.has(key(there));

    const solve = async () => {
        start = await maze.whereAmI();

        const todo = new Queue();
        todo.enqueue([start, "start"]);

        while (todo.length > 0) {
            const [here, from] = todo.dequeue();
            await maze.goTo(here);
            markShortestFrom(here, from);
            const isExit = await maze.isExit();
            if (isExit) {
                console.log(`Exit is at: ${key(here)}. Retracing steps...`);

                const steps = [here];
                while (true) {
                    const from = shortestFrom.get(key(steps[steps.length - 1]));
                    if (from === "start") {
                        break;
                    }
                    steps.push(from);
                }

                const path = steps.reverse()
                    .map(s => `(${key(s)})`)
                    .join(", ");
                console.log("SOLUTION:");
                console.log(path);
                maze.bye();
            }
            const availableDirs = await maze.look();
            for (const dir of availableDirs) {
                const there = move(here, dir);
                if (!beenThere(there)) {
                    todo.enqueue([there, here]);
                }
            }
        }

        maze.bye();
    }

    return { solve };

};


const main = async () => {

    const maze = createMazeClient(client);
    await maze.receiveWelcome();
    const solver = createSolver(maze);
    await solver.solve();

    // console.log(await maze.whereAmI());
    // console.log(await maze.isExit());
    // console.log(await maze.go("west"));
    // console.log(await maze.look());
    // console.log(await maze.goTo(0, 0));
    //
    // console.log(await maze.bye());
};

const client = new net.Socket();
client.connect(4321, "codechallenge-daemons.0x14.net", () => {
    main();
});


// const killTime = setTimeout(() => {
//     client.write("bye");
// }, 3000);

client.on("close", (data) => {
    console.log("Server closed connection.");
    // clearTimeout(killTime);
    client.destroy();
});
