'use strict';

describe('Filter: bodyTypeFilter', function () {

  // load the filter's module
  beforeEach(module('cupidCrawlerApp'));

  // initialize a new instance of the filter before each test
  var bodyTypeFilter;
  beforeEach(inject(function ($filter) {
    bodyTypeFilter = $filter('bodyTypeFilter');
  }));

  it('should return the input prefixed with "bodyTypeFilter filter:"', function () {
    var text = 'angularjs';
    expect(bodyTypeFilter(text)).toBe('bodyTypeFilter filter: ' + text);
  });

});
