const argType = {
    actor_definitions: 2,
    tests: 3
};

var actor_definitions = JSON.parse(process.argv[argType.actor_definitions]);
var tests = JSON.parse(process.argv[argType.tests]);

console.log(actor_definitions);
console.log(tests);

// load actors
var actor_classes = {};
for (var actor_name in actor_definitions) {
    var module = actor_definitions[actor_name][0][0];
    var class_name = actor_definitions[actor_name][0][1];
    if (!(class_name in actor_classes)) {
        actor_classes[class_name] = require(module);
    }
}

console.log(actor_classes);

// run tests


function run_test(test) {
    console.log(test);
}
