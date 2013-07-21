'use strict';

angular.module('cupidCrawlerApp')
  .controller('ProfilePicsCtrl', function ($scope) {
    
    $scope.currImg = $scope.profile.img_more[0];
    $scope.hoverImg = $scope.currImg;
    $scope.hoverImg.selected = true;
    
    $scope.setCurrImg = function(img) {
      $scope.currImg.selected = false;
      $scope.currImg = img;
      $scope.currImg.selected = true;
      $scope.hoverImg = $scope.currImg;
    };

    $scope.mouseOverImg = function(img) {
      $scope.hoverImg = img;
    };

    $scope.leaveImg = function() {
      $scope.hoverImg = $scope.currImg;
    };

  });
