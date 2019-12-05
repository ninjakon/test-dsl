const argType = {
    actor_definitions: 2,
    tests: 3
};

var actor_definitions = JSON.parse(process.argv[argType.actor_definitions]);
var tests = JSON.parse(process.argv[argType.tests]);

console.log(actor_definitions);
console.log(tests);

// load actors
var actors = {};
for (var actor_name in actor_definitions) {
    var module = actor_definitions[actor_name][0];
    const actor_class = require(module);
    actors[actor_name] = new actor_class();
}

console.log(actors);

// run tests


function run_test(test) {
    console.log(test);
}
