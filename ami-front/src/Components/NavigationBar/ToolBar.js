import React, {Component} from 'react';
import ToggleButton from './ToggleButton.js';
import Login from '../Login'
import './ToolBar.css';
import SideDrawer from './SideDrawer'

class ToolBar extends Component{
  constructor(props){
    super(props);
    
    this.sideDrawer = SideDrawer
  }

  render(){
    return (
    <header className="toolbar">
      <nav className="toolbar__navigation">
        <div className="toolbar__toggle-button">
          <ToggleButton click={this.sideDrawer.drawerClickHandler}/>
        </div>
        <div className="toolbar__logo">
          <a href="/">Aerial Multispectral Imaging</a>
        </div>
        <div className="spacer" />
        <div className="toolbar_navigation-items">
          <ul>
          <li>
              <button onClick={this.login}>Login</button>
            </li>
          </ul>
        </div>
      </nav>
    </header>
    )
  
  }
  }

export default ToolBar