'use strict';

describe('Filter: locationFilter', function () {

  // load the filter's module
  beforeEach(module('cupidCrawlerApp'));

  // initialize a new instance of the filter before each test
  var locationFilter;
  beforeEach(inject(function ($filter) {
    locationFilter = $filter('locationFilter');
  }));

  it('should return the input prefixed with "locationFilter filter:"', function () {
    var text = 'angularjs';
    expect(locationFilter(text)).toBe('locationFilter filter: ' + text);
  });

});
