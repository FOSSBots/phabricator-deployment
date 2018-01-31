'use strict';
const assert = require( 'assert' ),
	HomePage = require( '../pageobjects/home.page' ),
	SearchPage = require( '../pageobjects/search.page' );

describe( 'Homepage', function () {

	it( 'when searching for db1110 from homepage, search page should open', function () {

		HomePage.search( 'db1110' );

		assert( SearchPage.search.isExisting() );

	} );

} );
