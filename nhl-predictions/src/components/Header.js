import React, { Fragment, useState, useEffect } from "react";
import '../App.css';

const Header = () => {

return (
    <Fragment>
        <div class="header">
            <a class="headerItem" href="/schedule">
                <h1 class="headerText">Schedule</h1>
            </a>
            <a class="headerItem" href="/">
                <h1 class="headerText">Predictor</h1>
                </a>
            <a class="headerItem" href="/rankings">
                <h1 class="headerText">Power Rankings</h1>
            </a>
        </div>
        </Fragment>
    );
};

export default Header;