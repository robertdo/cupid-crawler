'use strict';

angular.module('cupidCrawlerApp')
  .controller('ProfileModalCtrl', function ($scope) {
    
    $scope.open = function() {
      $scope.shouldBeOpen = true;
    };

    $scope.close = function() {
      $scope.closeMsg = 'I was closed at: ' + new Date();
      $scope.shouldBeOpen = false;
    };

    $scope.opts = {
      backdropFade: true,
      dialogFade: true
    };

  });
