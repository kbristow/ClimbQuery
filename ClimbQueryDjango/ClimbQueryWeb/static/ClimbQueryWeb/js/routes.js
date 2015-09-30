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
                    {this.props.getCragCallback(fields.crag)}
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

    _getCrag: function(cragId){
        if(this.props.crags.hasOwnProperty(cragId)){
            return this.props.crags[cragId];
        }
        return cragId;
    },

    render: function(){
        var routeNodes = this.props.routes.map(function (route){
            return (
            <Route route={route} getCragCallback={this._getCrag}/>
            );
        }.bind(this));
        return (
            <div>
                <table className="table-striped" id="RouteListTable">
                    <tbody>
                        <tr>
                            <th className="col-lg-2">
                                Name
                            </th>
                            <th className="col-lg-2">
                                Crag
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
                            <th className="col-lg-4">
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
        return {routes: [], crags: {}};
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
            url: this.props.urlRoutes,
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
    _getCragData: function (data){
        var pkCragMap = {};
        for (var i = 0; i < data.length; i++){
            pkCragMap[data[i].pk] = data[i];
        }
        return pkCragMap;
    },
    _convertToCragMap : function(cragData){
        var cragMap = {};
        for (var i in cragData){
            cragMap[cragData[i].pk] = this._pullFullName(cragData[i], cragData);
        }
        return cragMap;
    },
    _pullFullName : function(crag, cragMap){
        if (crag.fields.parent_crag == null){
            return crag.fields.name;
        }
        else{
            return this._pullFullName(cragMap[crag.fields.parent_crag], cragMap) + " / " + crag.fields.name;
        }
    },
    _loadCragsFromServer: function(climbingArea){
        var requestData = {climbingArea: climbingArea};
        $.ajax({
            method: "POST",
            url: this.props.urlCrags,
            data: JSON.stringify(requestData),
            dataType: 'json',
            cache: false,
            success: function(data) {
                var cragData = this._getCragData(data);
                var cragMap = this._convertToCragMap(cragData);
                this.setState({crags: cragMap});
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
                <RouteSearchBox
                    onSearch={this._onSearch}
                    ref="routeSearchRef"
                    updateCragsCallback={this._loadCragsFromServer}
                    crags = {this.state.crags}
                />
                <h1>Routes</h1>
                <RouteList
                    routes = {this.state.routes}
                    crags = {this.state.crags}
                />
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


var StyleSelector = React.createClass({

    getInitialState: function() {
        var styleOptions = {
            "Any" : "",
            "Sport" : "Sport",
            "Trad" : "Trad"
        };
        var styles = [];
        for (var key in styleOptions){
            styles.push(<option value={styleOptions[key]}>{key}</option>);
        }
        return {styles: styles};
    },

    componentDidMount: function() {
        $("#" + this.props.id).select2({ width: '100%' });
    },

    render: function(){
        return(
            <select className={this.props.className} id={this.props.id}>
                {this.state.styles}
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

    componentDidMount: function(){
        var climbingAreaSelect =  $("#" + this.props.id);
        var select2 = climbingAreaSelect.select2().data("select2");
        climbingAreaSelect.on("change", this._selectorOnChange);
        this._loadClimbingAreasFromServer();
    },
    _selectorOnChange:function(){
        this.props.changeCallback($("#climbingAreaSelect").val());
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
        //TODO: Need to move this up in the component hierarchy?
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
    _convertToFullCragNames : function(cragMap){
        var crags = [];
        for (var i in cragMap){
            crags.push({id: i, text: cragMap[i]});
        }
        crags.sort(this._compareCragResult);
        return crags;
    },
    _createSelectOptions: function(data){
        var options = [];
        for (var i = 0; i < data.length; i++){
            options.push(<option value={data[i].id}>{data[i].text}</option>);
        }
        return options;
    },

    render: function(){
        var sortedCrags = this._convertToFullCragNames(this.props.crags);
        var cragOptions = this._createSelectOptions(sortedCrags);
        return(
            <select className={this.props.className} id={this.props.id} multiple="multiple" placeholder="Select a Crag">
                {cragOptions}
            </select>
        );
    }

});

var RouteSearchBox = React.createClass({

    _climbingAreaSelectChange: function(climbingArea){
        this.props.updateCragsCallback(climbingArea);
    },
    _getSearchOptions: function(){
        var searchOptions = {};
        searchOptions["climbingArea"] = $("#climbingAreaSelect").val();
        searchOptions["crags"] = $("#cragSelect").val();
        searchOptions["minGrade"] = $("#minGradeSelector").val();
        searchOptions["maxGrade"] = $("#maxGradeSelector").val();
        searchOptions["minStars"] = $("#minStarSelector").val();
        searchOptions["style"] = $("#styleSelector").val();
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
                        <ClimbingAreaSearch id="climbingAreaSelect" url="/ClimbQueryService/ClimbingArea/" changeCallback={this._climbingAreaSelectChange} ref="climbingAreaSelectRef" />
                    </dd>
                    
                    <dt>
                        Crag
                    </dt>
                    <dd>
                        <CragSearch id="cragSelect" crags={this.props.crags} />
                    </dd>

                    <dt>
                        Climbing Style
                    </dt>
                    <dd>
                        <StyleSelector id="styleSelector" initial="40"/>
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
    <RouteListBox urlRoutes="/ClimbQueryService/Route/" urlCrags="/ClimbQueryService/Crag/"/>,
    document.getElementById('react_container')
);