const argType = {
    actor_definitions: 2,
    before_all: 3,
    befores: 4,
    tests: 5,
    afters: 6,
    after_all: 7,
    verbose: 8
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

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Testing Arguments */
const actor_definitions = JSON.parse(process.argv[argType.actor_definitions]);
const before_all = JSON.parse(process.argv[argType.before_all]);
const befores = JSON.parse(process.argv[argType.befores]);
const tests = JSON.parse(process.argv[argType.tests]);
const afters = JSON.parse(process.argv[argType.afters]);
const after_all = JSON.parse(process.argv[argType.after_all]);
const verbose = process.argv[argType.verbose] === 'True';

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Log */
var log = {
    raw_text: '',
    actor_table: null
};

function print_if_verbose(msg, tb_lvl=0) {
    if (verbose) {
        for (var i = 0; i < tb_lvl; i++) {
            log.raw_text += '\t';
        }
        log.raw_text += msg + tText.ENDC + '\n';
    }
}

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Test Report */
var test_report = {
    BA: [],
    TC: 0,
    CT: [null, []],
    ST: [],
    FT: [],
    AA: []
};

add_error_fun = null;

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Step Processing */
function process_steps(steps, is_ba=false, callback) {
    const recursive_step = (i) => {
        if (i < steps.length) {
            if (is_ba) {
                print_if_verbose(tText.INFO + '"' + steps[i][0] + '" OK', tb_lvl=2);
            }
            process_step(steps[i][0], steps[i][1], i + 1, recursive_step);
        } else {
            callback();
        }
    };
    recursive_step(0);
}

function process_step(type, args, i, callback) {
    switch (type) {
        case 'AssertStep':
            process_assert_step(args, i, callback);
            break;
        case 'AssignStep':
            process_assign_step(args, i, callback);
            break;
        case 'CallStep':
            process_call_step(args, i, callback);
            break;
        case 'TimeStep':
            process_time_step(args, i, callback);
            break;
    }
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Testing */
function process_ba_aa(type, steps, callback) {
    var is_ba = type.localeCompare('BA') === 0;
    print_if_verbose(tText.INFO + (is_ba ? 'Running BeforeAll' : 'Running AfterAll'));
    add_error_fun = function(l, e) { test_report[type].push([l + tText.ENDC, e + tText.ENDC]) };
    process_steps(steps, is_ba=true, callback);
}

function process_before_after_test(type, blocks, references) {
    if (references.length > 0) {
        print_if_verbose(tText.INFO + 'Running ' + type, tb_lvl=1);
    }
    add_error_fun = function (l, e) {
        test_report['CT'][1].push([tText.INFO + 'In ' + type + ' Clause: ' + l + tText.ENDC, e + tText.ENDC])
    };
    for (var i = 0; i < references.length; i++) {
        process_steps(blocks[references[i]], true);
    }
}

function process_tests(tests, callback) {
    const recursive_test= (i) => {
        if (i < tests.length) {
            if (is_ba) {
                print_if_verbose(tText.INFO + '"' + tests[i][0] + '" OK', tb_lvl=2);
            }
            process_test(tests[i][0], tests[i][1], i + 1, recursive_test);
        } else {
            callback();
        }
    };
    recursive_step(0);
}

function process_test() {
    for (var i = 0; i < tests.length; i++) {
        log.raw_text += tText.INFO + 'Running ' + test_name + tText.ENDC + '\n';
        var test_name = tests[i];
        test_report.CT = [test_name, []];
        var test = tests[test_name];

        // run befores
        process_before_after_test('Before', befores, test[testBlock.before]);

        // run test
        var steps = test[testBlock.execute];
        print_if_verbose(tText.INFO + 'Executing Test', tb_lvl=1);
        process_steps(steps);

        // run afters
        process_before_after_test('After', afters, test[testBlock.after]);

        // update test report
        var current_test = test_report.CT[0];
        var errors = test_report.CT[1];
        if (errors.length === 0) {
            test_report.ST.push(current_test);
        } else {
            test_report.FT.push(test_report.CT);
        }
        test_report.TC += 1;
        test_report.CT = [null, []];
    }
}

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * Specified Step Processing */
function process_assert_step(args, i, callback) {
    actor_name = args[0];
    actor = actors[actor_name];
    attribute = args[1];
    expected_value = args[2];
    actual_value = actor[attribute];

    is_ok = actual_value === expected_value;
    message = style_assertion(is_ok, actor_name, attribute, expected_value, actual_value);
    if (!is_ok) {
        add_error_fun('IDK', message + tText.ENDC);
    }
    print_if_verbose(message, tb_lvl=2);
    callback(i);
}

function process_assign_step(args, i, callback) {
    actor = actors[args[0]];
    attribute = args[1];
    value = args[2];
    actor[attribute] = value;
    callback(i);
}

function process_call_step(args, i, callback) {
    actor = actors[args[0]];
    method = args[1];
    params = [];
    for (var j = 0; j < args[2].length; j++) {
        is_actor = args[2][j][0];
        param = args[2][j][1];
        is_actor ? params.push(actors[param]) : params.push(param);
    }
    actor[method](...params);
    callback(i);
}

function process_time_step(args, i, callback) {
    setTimeout(() => callback(i), args[0]);
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Assertions */
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
        color + suffix
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * Actors */
// Load actors by specifying modules, instantiating classes and setting attributes.
var actors = {};
var actor_tbl = [];
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

    // append to actor table
    actor_tbl.push([actor_name, module, actors[actor_name]]);
}
log.actor_table = actor_tbl;

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Testing */
process_ba_aa('BA', before_all, () => {
    // Run tests.
    for (var i = 0; i < tests.length; i++) {
        log.raw_text += tText.INFO + 'Running ' + test_name + tText.ENDC + '\n';
        var test_name = tests[i];
        test_report.CT = [test_name, []];
        var test = tests[test_name];

        // run befores
        process_before_after_test('Before', befores, test[testBlock.before]);

        // run test
        var steps = test[testBlock.execute];
        print_if_verbose(tText.INFO + 'Executing Test', tb_lvl=1);
        process_steps(steps);

        // run afters
        process_before_after_test('After', afters, test[testBlock.after]);

        // update test report
        var current_test = test_report.CT[0];
        var errors = test_report.CT[1];
        if (errors.length === 0) {
            test_report.ST.push(current_test);
        } else {
            test_report.FT.push(test_report.CT);
        }
        test_report.TC += 1;
        test_report.CT = [null, []];
    }

    process_ba_aa('AA', after_all, () => {
       console.log(JSON.stringify({log: log, test_report: test_report}));
    });
});

