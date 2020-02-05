import React, {Component} from 'react'
import styles from '../Components/Style/NavBarStyle.css'
import backend from '../globals'
export default class NavBar extends Component{
    constructor(props){
        super(props);
        this.handleToggleSideBar=this.handleToggleSideBar.bind(this);
    }
    handleToggleSideBar(){
        this.props.parent.sideBarRef.current.setState({hidden:!this.props.parent.sideBarRef.current.state.hidden})
        if(this.props.parent.state.sidebarClass==='hidden'){
            this.props.parent.setState({sidebarClass:'visible'});
        }
        else{
            this.props.parent.setState({sidebarClass:'hidden'});
        }
    }
    render(){
        return (
            <nav className='navbar'> 
                <img onClick={this.handleToggleSideBar} className='icon' alt='menu button' src='https://cdn4.iconfinder.com/data/icons/wirecons-free-vector-icons/32/menu-alt-512.png'/>
                <header className='navbar-header'>skyprecision.net</header>
            </nav>
        )
    }
}