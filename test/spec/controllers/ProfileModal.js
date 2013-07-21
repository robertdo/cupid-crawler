'use strict';

describe('Controller: ProfileModalCtrl', function () {

  // load the controller's module
  beforeEach(module('cupidCrawlerApp'));

  var ProfileModalCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ProfileModalCtrl = $controller('ProfileModalCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
