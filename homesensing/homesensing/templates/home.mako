<%inherit file="layout.mako"/>

<%block name="title">
    Temperature logger
</%block>


<%block name="main">
    <div class="jumbotron">
        <h1 class="display-4">Environmental measurements</h1>
        <p class="lead">Raspberry Pi sensors from across the house</p>
        <hr class="my-4">
        <p>TODO: re-add URL query for specific range.</p>
    </div>
    <div class="row">
        <div class="col-12">
            <h3>Latest values</h3>

            <div id="latest" class="card-columns"></div>
            <p>View:</p>
            <div class="btn-group" role="group" id="changeRange">
                <button type="button" class="btn btn-secondary" data-delta="1">Last 24 hours</button>
                <button type="button" class="btn btn-secondary" data-delta="3">Last 3 days</button>
                <button type="button" class="btn btn-secondary" data-delta="7">Last week</button>
                <button type="button" class="btn btn-secondary" data-delta="30">Last Month</button>
                <button type="button" class="btn btn-secondary" data-delta="365">Last Year</button>
            </div>
        </div>
    </div>
    <div id="graph" style="height:100vh;width:100vw;"></div>
</%block>


<%block name="script">
    <script type="text/javascript">
        <%include file="home.js"/>
    </script>
</%block>