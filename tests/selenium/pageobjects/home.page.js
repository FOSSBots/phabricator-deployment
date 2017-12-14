'use strict';
const Page = require( './page' );

class HomePage extends Page {

	get searchBox() { return browser.element( '[name="query"]' ); }

	open() {
		super.open( '' );
	}

	search( term ) {
		this.open();
		this.searchBox.setValue( `${term}\n` );
	}
}
module.exports = new HomePage();
