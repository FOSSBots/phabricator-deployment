'use strict';
const Page = require( './page' );

class HomePage extends Page {
	get searchButton() { return browser.element( '[class="phabricator-main-menu-search-button"]'); }
	get searchBox() { return browser.element( '[name="query"]' ); }

	open() {
		super.open( '' );
	}

	search( term ) {
		this.open();
		browser.setViewportSize({
			width:1200,
			height: 500
		},false);
		//this.searchButton.click();
		this.searchBox.setValue( `${term}\n` );
	}
}
module.exports = new HomePage();
