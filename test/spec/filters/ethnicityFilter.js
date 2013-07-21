'use strict';

describe('Filter: ethnicityFilter', function () {

  // load the filter's module
  beforeEach(module('cupidCrawlerApp'));

  // initialize a new instance of the filter before each test
  var ethnicityFilter;
  beforeEach(inject(function ($filter) {
    ethnicityFilter = $filter('ethnicityFilter');
  }));

  it('should return the input prefixed with "ethnicityFilter filter:"', function () {
    var text = 'angularjs';
    expect(ethnicityFilter(text)).toBe('ethnicityFilter filter: ' + text);
  });

});
