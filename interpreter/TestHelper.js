var actor_definitions = JSON.parse(process.argv[2]);
var actor_classes = {};

console.log(actor_definitions);

// load actors
for (var actor_name in actor_definitions) {
    var module = actor_definitions[actor_name][0][0];
    var class_name = actor_definitions[actor_name][0][1];
    if (!(class_name in actor_classes)) {
        actor_classes[class_name] = require(module);
    }
}

console.log(actor_classes);

function run_test(test) {
    console.log(test);
}
