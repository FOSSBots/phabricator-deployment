# Selenium tests

More documentation is available at https://www.mediawiki.org/wiki/Selenium/Node.js

## Setup

    npm install

## Start Chromedriver and run all tests

Run all tests (from repository root):

    npm run selenium

## Start Chromedriver

To run only some tests, you first have to start Chromedriver in one terminal tab (or window):

    chromedriver --url-base=wd/hub --port=4444

## Run test(s) from one file

Then, in another terminal tab (or window) run this from repository root:

    ./node_modules/.bin/wdio --spec tests/selenium/specs/FILE-NAME.js

`wdio` is a dependency that you have installed with `npm install`.

## Run specific test(s)

To run only test(s) which name contains string TEST-NAME, run this from repository root:

    ./node_modules/.bin/wdio --spec tests/selenium/specs/FILE-NAME.js --mochaOpts.grep TEST-NAME

Make sure Chromedriver is running when executing the above command.
