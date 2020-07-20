'use strict';
const Page = require( './page' );

class HomePage extends Page {
	get searchButton() { return $( '[class="phabricator-main-menu-search-button"]' ); }
	get searchBox() { return $( '[name="query"]' ); }

	open() {
		super.open( '' );
	}

	search( term ) {
		this.open();
		browser.setWindowSize( 1200, 500 );
		// this.searchButton.click();
		this.searchBox.setValue( `${term}\n` );
	}
}
module.exports = new HomePage();
