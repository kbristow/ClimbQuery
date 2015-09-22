var Route = React.createClass({

    _getStarRepresentation: function(nStars){
        var stars = [];
        for (var i = 0; i < nStars; i ++){
            stars.push(<span className='glyphicon glyphicon-star'></span>);
        }
        return stars;
    },
    _getDraws: function(nDraws){
        var draws = nDraws;
        if (parseInt(nDraws) == 0){
            draws = '-';
        }
        return draws;
    },

    render: function() {
        var fields = this.props.route.fields;
        var stars = this._getStarRepresentation(fields.stars);
        var draws = this._getDraws(fields.draws);
        return (
            <tr>
                <td>
                    {fields.name}
                </td>
                <td>
                    {fields.grade}
                </td>
                <td>
                    {stars}
                </td>
                <td>
                    {fields.climbing_style}
                </td>
                <td>
                    {draws}
                </td>
                <td>
                    {fields.description}
                </td>
            </tr>
        );
    }

});

var RouteList = React.createClass({

    render: function(){
        var routeNodes = this.props.data.map(function (route){
            return (
            <Route route={route}/>
            );
        });
        return (
            <div>
                <table className="table-striped" id="RouteListTable">
                    <tbody>
                        <tr>
                            <th className="col-lg-2">
                                Name
                            </th>
                            <th className="col-lg-1">
                                Grade
                            </th>
                            <th className="col-lg-1">
                                Stars
                            </th>
                            <th className="col-lg-1">
                                Climbing Style
                            </th>
                            <th className="col-lg-1">
                                Draws/Anchors
                            </th>
                            <th className="col-lg-6">
                                Description
                            </th>
                        </tr>
                        {routeNodes}
                    </tbody>
                </table>
            </div>
        );
    }

});


var RouteListBox = React.createClass({
    
    getInitialState: function() {
        return {routes: []};
    },
    
    componentDidMount: function() {
        $('#RouteListTable').stacktable();
    },
    componentDidUpdate: function(){
        $('#RouteListTable').stacktable();
    },
    
    _onSearch: function(){
        var searchOptions = this.refs.routeSearchRef._getSearchOptions();
        this._loadRoutesFromServer(searchOptions);
    },
    _loadRoutesFromServer: function(searchOptions) {
        $.ajax({
            method: "POST",
            url: this.props.url,
            data: JSON.stringify(searchOptions),
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({routes: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    
    
    render: function() {
        return (
            <div className="routeListBox">
                <h1>Search Details</h1>
                <RouteSearchBox onSearch={this._onSearch} ref="routeSearchRef"/>
                <h1>Routes</h1>
                <RouteList data = {this.state.routes}/>
            </div>
        );
    }

});

var GradeSelector = React.createClass({

    getInitialState: function() {
        var grades = [];
        for (var i = 0; i < 40; i ++){
            grades.push(<option val={i+1}>{i+1}</option>);
        }
        return {grades: grades};
    },

    componentDidMount: function() {
        var selector = $("#" + this.props.id);
        selector.val(this.props.initial);
        selector.select2({width: '100%'});
    },

    render: function(){
        return(
            <select className={this.props.className} id={this.props.id}>
                {this.state.grades}
            </select>
        );
    }

});

var StarSelector = React.createClass({

    getInitialState: function() {
        var stars = [];
        for (var i = 0; i < 6; i ++){
            stars.push(<option value={i}>{i}</option>);
        }
        return {stars: stars};
    },

    componentDidMount: function() {
        $("#" + this.props.id).select2({ width: '100%' });
    },

    render: function(){
        return(
            <select className={this.props.className} id={this.props.id}>
                {this.state.stars}
            </select>
        );
    }

});


var SearchButton = React.createClass({

    render: function(){
        return(
            <a className={this.props.className} onClick={this.props.onClick}>Search</a>
        );
    }

});

var ClimbingAreaSearch = React.createClass({
    
    getInitialState: function() {
        return {climbingAreas: []};
    },

    componentDidMount: function() {
        this._loadClimbingAreasFromServer();
    },

    _createSelectOptions: function(data){
        //Empty option for placeholder
        var options = [<option></option>];
        for (var i = 0; i < data.length; i++){
            var fields = data[i].fields;
            options.push(<option value={data[i].pk}>{fields.country} / {fields.name}</option>);
        }
        return options;
    },
    _loadClimbingAreasFromServer: function(){
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                var climbingAreas = this._createSelectOptions(data);
                this.setState({climbingAreas: climbingAreas});
                //Update the place holder
                var select2 = $("#" + this.props.id).select2({ width: '100%' }).data("select2");
                select2.setPlaceholder();
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    _getSelectedClimbingArea:function(){
        return $("#" + this.props.id).val();
    },
    
    render: function(){
        return(
            <select className={this.props.className} id={this.props.id} placeholder="Select a Climbing Area">
                {this.state.climbingAreas}
            </select>
        );
    }

});


var CragSearch = React.createClass({

    getInitialState: function() {
        return {crags: [], climbingArea: ""};
    },

    componentDidMount: function() {
        //Turn select into select2 box
        var select2 = $("#" + this.props.id).select2({ width: '100%', allowClear: true}).data("select2");
    },

    _compareCragResult: function (cragA, cragB){
      if (cragA.text < cragB.text)
        return -1;
      if (cragA.text > cragB.text)
        return 1;
      return 0;
    },
    _getCragMap: function (data){
        var pkCragMap = {};
        for (var i = 0; i < data.length; i++){
            pkCragMap[data[i].pk] = data[i];
        }
        return pkCragMap;
    },
    _convertToFullCragNames : function(cragMap){
        var crags = [];
        for (var i in cragMap){
            crags.push({id: i, text: this._pullFullName(cragMap[i], cragMap)});
        }
        crags.sort(this._compareCragResult);
        return crags;
    },
    _pullFullName : function(crag, cragMap){
        if (crag.fields.parent_crag == null){
            return crag.fields.name;
        }
        else{
            return this._pullFullName(cragMap[crag.fields.parent_crag], cragMap) + " / " + crag.fields.name;
        }
    },
    _createSelectOptions: function(data){
        var options = [];
        for (var i = 0; i < data.length; i++){
            options.push(<option value={data[i].id}>{data[i].text}</option>);
        }
        return options;
    },
    _loadCragsFromServer: function(climbingArea){
        climbingArea = typeof climbingArea !== 'undefined' ? climbingArea : "";
        if (climbingArea!==""){
            var select2 = $("#" + this.props.id).select2({ width: '100%', allowClear: true}).data("select2");
            var requestData = {climbingArea: climbingArea};
            $.ajax({
                method: "POST",
                url: this.props.url,
                data: JSON.stringify(requestData),
                dataType: 'json',
                cache: false,
                success: function(data) {
                    var cragMap = this._getCragMap(data);
                    var fullCragNames = this._convertToFullCragNames(cragMap);
                    var crags = this._createSelectOptions(fullCragNames);
                    this.setState({crags: crags});
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this)
            });
        }
    },

    render: function(){
        return(
            <select className={this.props.className} id={this.props.id} multiple="multiple" placeholder="Select a Crag">
                {this.state.crags}
            </select>
        );
    }

});

var RouteSearchBox = React.createClass({

    componentDidMount: function() {
        var climbingAreaSelect =  $("#climbingAreaSelect");
        var select2 = climbingAreaSelect.select2().data("select2");
        climbingAreaSelect.on("change", this._climbingAreaSelectChange);
    },

    _climbingAreaSelectChange: function(){
        var climbingArea = this.refs.climbingAreaSelectRef._getSelectedClimbingArea();
        this.refs.cragSelectRef._loadCragsFromServer(climbingArea);
    },
    _getSearchOptions: function(){
        var searchOptions = {};
        searchOptions["climbingArea"] = $("#climbingAreaSelect").val();
        searchOptions["crags"] = $("#cragSelect").val();
        searchOptions["minGrade"] = $("#minGradeSelector").val();
        searchOptions["maxGrade"] = $("#maxGradeSelector").val();
        searchOptions["minStars"] = $("#minStarSelector").val();
        return searchOptions;
    },

    render: function(){
        return(
            <div>
                <dl>
                    <dt>
                        Climbing Area
                    </dt>
                    <dd>
                        <ClimbingAreaSearch id="climbingAreaSelect" url="/ClimbQueryService/ClimbingArea/" ref="climbingAreaSelectRef" />
                    </dd>
                    
                    <dt>
                        Crag
                    </dt>
                    <dd>
                        <CragSearch id="cragSelect" url="/ClimbQueryService/Crag/" ref="cragSelectRef" />
                    </dd>
                    
                    <dt>
                        Minimum Grade
                    </dt>
                    <dd>
                        <GradeSelector id="minGradeSelector" initial="1"/>
                    </dd>
                    
                    <dt>
                        Maximum Grade
                    </dt>
                    <dd>
                        <GradeSelector id="maxGradeSelector" initial="40"/>
                    </dd>
                    <dt>
                        Minimum Stars
                    </dt>
                    <dd>
                        <StarSelector id="minStarSelector"/>
                    </dd>
                </dl>
                <br/>
                <SearchButton className="btn btn-default" onClick={this.props.onSearch}/>
            </div>
        );
    }

});

React.render(
    <RouteListBox url="/ClimbQueryService/Route/"/>,
    document.getElementById('react_container')
);