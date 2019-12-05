const argType = {
    actor_definitions: 2,
    tests: 3,
    verbose: 4
};

const testBlock = {
  before: 0,
  execute: 1,
  after: 2
};

const tText = {
    INFO: '\033[94m',
    OK: '\033[92m',
    WARN: '\033[93m',
    FAIL: '\033[91m',
    BOLD: '\033[1m',
    UL: '\033[4m',
    ENDC: '\033[0m'
};

/**
 * Output variables.
 */
var log = '';
var test_report = {

};

function style_assertion(is_ok, actor_name, attribute, expected_value, actual_value) {
    if (is_ok) {
        prefix = tText.OK + 'Assertion OK: ' + tText.ENDC;
        infix = 'and was';
        suffix = '.';
        color = tText.OK;

    } else {
        prefix = tText.WARN + 'Assertion ' + tText.BOLD + 'ERROR\n' + tText.ENDC;
        infix = 'but was';
        suffix = '!';
        color = tText.FAIL;
    }
    return prefix + color + 'Expected ' + tText.BOLD + ` ${actor_name}[${attribute}]` + tText.ENDC +
        color + ' == ' + tText.BOLD + `${expected_value} ` + tText.ENDC +
        color + infix + tText.BOLD + ` ${actual_value}` + tText.ENDC +
        color + suffix + tText.ENDC + '\n'
}

/**
 * Get arguments for testing.
 */
var actor_definitions = JSON.parse(process.argv[argType.actor_definitions]);
var tests = JSON.parse(process.argv[argType.tests]);
var verbose = process.argv[argType.verbose] === 'True';

/**
 * Load actors by specifying modules, instantiating classes and setting attributes.
 */
var actors = {};
for (var actor_name in actor_definitions) {
    // instantiate classes
    var module = actor_definitions[actor_name][0];
    const actor_class = require(module);
    actors[actor_name] = new actor_class();

    // set pre-defined attributes
    var attributes = actor_definitions[actor_name][1];
    for (var i = 0; i < attributes.length; i++) {
        var attribute_name = attributes[i][0];
        var value = attributes[i][1];
        actors[actor_name][attribute_name] = value;
    }
}

/**
 * Run tests.
 */
for (var test_name in tests) {
    log += 'Running ' + test_name + '\n';
    var steps = tests[test_name][testBlock.execute];
    for (var i = 0; i < steps.length; i++) {
        step = steps[i];
        type = step[0];
        args = step[1];

        switch (type) {
            case 'AssertStep':
                actor_name = args[0];
                actor = actors[actor_name];
                attribute = args[1];
                expected_value = args[2];
                actual_value = actor[attribute];

                is_ok = actual_value === expected_value;
                message = style_assertion(is_ok, actor_name, attribute, expected_value, actual_value)
                if (verbose) {
                    log += message;
                }
                break;
            case 'AssignStep':
                actor = actors[args[0]];
                attribute = args[1];
                value = args[2];
                actor[attribute] = value;
                break;
            case 'CallStep':
                actor = actors[args[0]];
                method = args[1];
                params = [];
                for (var j = 0; j < args[2].length; j++) {
                    is_actor = args[2][j][0];
                    param = args[2][j][1];
                    is_actor ? params.push(actors[param]) : params.push(param);
                }
                actor[method](...params);
                break;
            case 'TimeStep':
                // await sleep(500);
                break;
        }
    }
}

console.log(log);
