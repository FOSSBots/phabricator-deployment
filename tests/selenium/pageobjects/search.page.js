'use strict';
const Page = require( './page' );

class SearchPage extends Page {

	get search() { return browser.element( '[name="__submit__"]' ); }

}
module.exports = new SearchPage();
