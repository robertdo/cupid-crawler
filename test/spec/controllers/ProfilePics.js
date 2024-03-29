'use strict';

describe('Controller: ProfilePicsCtrl', function () {

  // load the controller's module
  beforeEach(module('cupidCrawlerApp'));

  var ProfilePicsCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ProfilePicsCtrl = $controller('ProfilePicsCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
