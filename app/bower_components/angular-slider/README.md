angular-slider (WIP)
====================

Slider directive implementation for AngularJS, without jQuery dependencies. Requires AngularJS v1.1.4 or higher (optional isolate scope bindings support).

### Example:

    <ul>
        <li ng-repeat="item in items">
            <p>Name: {{item.name}}</p>
            <p>Cost: {{item.cost}}</p> 
            <slider floor="100" ceiling="1000" step="50" precision="2" ng-model="item.cost"></slider>
        </li>
    </ul>

### Range:

    <ul>
        <li ng-repeat="position in positions">
            <p>Name: {{position.name}}</p>
            <p>Minimum Age: {{position.minAge}}</p> 
            <p>Maximum Age: {{position.maxAge}}</p> 
            <slider floor="10" ceiling="60" ng-model-low="position.minAge" ng-model-high="position.maxAge"></slider>
        </li>
    </ul>

### Known issues:
  
1. When applying filters or orders within an ng-repeat directive, the element can abruptly change its position when the value attached to the slider causes a filter to activate or the order to change. 
Example: In the above snippet, it would be a very bad idea to order the list by item.cost.

### Roadmap:

1. Touch events support
2. Smooth curve heterogeneity