'use strict';
const Page = require( './page' );

class HomePage extends Page {

	get content() { return browser.element( '#wpTextbox1' ); }

	}

}
module.exports = new HomePage();
