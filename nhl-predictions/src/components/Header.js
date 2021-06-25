import React, { Fragment } from "react";
import { Link } from "react-router-dom";
import '../App.css';

const Header = () => {

return (
    <Fragment>
        <div class="header">

            <Link to="/schedule" class="headerItem"><h1 class="headerText">Schedule</h1></Link>

            <Link to="/" class="headerItem"><h1 class="headerText">Predictor</h1></Link>
            <Link to="/rankings" class="headerItem"><h1 class="headerText">Power Rankings</h1></Link>
        </div>
        </Fragment>
    );
};

export default Header;