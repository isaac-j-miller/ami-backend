import React from 'react';
import Map from './Components/Map'
import NavBar from './Components/NavBar' 
import SideBar from './Components/SideBar'
import Login from './Components/Login'
import Scale from './Components/Scale'
//import Uploader from './Components/Uploader'
import axios from 'axios'
import styles from './Components/Style/AppStyle.css'
import backend from './globals'
class App extends React.Component {
  constructor(props){
    super(props);
    this.loginRef = React.createRef();
    this.toolBarRef = React.createRef();
    this.sideBarRef = React.createRef();
    this.mapRef = React.createRef();
    this.scaleRef = React.createRef();
    this.uploaderRef = React.createRef();
    this.getLoginClassName = this.getLoginClassName.bind(this);
    this.renderScale = this.renderScale.bind(this);
  }
  state = {
      sideDrawerOpen: false,  
      user: '',
      fields: [],
      activeField:'',
      activeDate:'',
      overlays:[],
      activeOverlay:'',
      loggedIn: false,
      origins: null
  } 
  componentDidMount(){
    console.log(backend)
    axios.get(`${backend.value}/overlays/req/possible_overlays/?`)
        .then(res =>{
            const info = res.data;
            this.setState({overlays:info.overlays});
            //console.log('overlaysrequest:')
            //console.log(info);
            this.sideBarRef.current.setState({overlays:info.overlays});
            this.sideBarRef.current.getOverlays();
        })
        .catch(function(error){
            console.warn(error);
        });
  }
  setActiveField(field){
    this.setState({activeField:field})
  }
  updateSideBar(){
    this.sideBarRef.current.setState({user:this.state.user, fields:this.state.fields})
  }
  getLoginClassName(){
    if(!this.state.loggedIn){
      return 'login-wrapper-large'
    }
    else{
      return 'login-wrapper-hidden'
    }
  }
  renderMap(){
    if(this.state.loggedIn){
      return(<Map parent={this} id='map' ref={this.mapRef}/>)
    }
    else{
      return <div/>
    }
  }
  renderScale(){
    if(this.state.loggedIn){
      return(<Scale parent={this} id='scale' ref={this.scaleRef}/>)
    }
    else{
      return <div/>
    }
  }
  renderUpload(){
    //return <Uploader parent={this} id='uploader' ref={this.uploaderRef}></Uploader>
    return <div/>
  }
  render() {
   return (
     <div>
      <div className={this.getLoginClassName()}>
        <Login parent={this} id='login' ref={this.loginRef}/>
      </div>
      <div className='nav-bar-wrapper'>
        <NavBar parent={this} id='toolbar' ref={this.toolBarRef}/>
      </div>
      <div className='side-bar-wrapper'>
        <SideBar parent={this} id='sidebar' ref={this.sideBarRef}/>
      </div>
      <div className='scale-wrapper'>
        {this.renderScale()}
      </div>
      <div className='map-wrapper'>
        {this.renderMap()}
      </div>
      <div className='uploader-wrapper'>
        {this.renderUpload()}
      </div>
     </div>
   )
  }
}

export default App
