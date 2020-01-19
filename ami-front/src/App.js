import React from 'react';
import Map from './Components/Map.js'
import ToolBar from './Components/NavigationBar/ToolBar.js' 
import SideBar from './Components/SideBar'
import Login from './Components/Login'
import axios from 'axios'

class App extends React.Component {
  constructor(props){
    super(props);
    this.loginRef = React.createRef();
    this.toolBarRef = React.createRef();
    this.sideBarRef = React.createRef();
    this.mapRef = React.createRef();
  
  }
  state = {
      sideDrawerOpen: false,  
      user: '',
      fields: [],
      activeField:'',
      activeDate:'',
      overlays:[],
      activeOverlay:''
  }
  componentDidMount(){
    axios.get(`http://localhost:8000/overlays/req/possible_overlays/?`)
        .then(res =>{
            const info = res.data;
            this.state.overlays=info.overlays;
            console.log('overlaysrequest:')
            console.log(info);
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
  render() {
   return (
     <div>
       <Login parent={this} id='login' ref={this.loginRef}/>
       <ToolBar parent={this} id='toolbar' ref={this.toolBarRef}/>
       <SideBar parent={this} id='sidebar' ref={this.sideBarRef}/>
       <Map parent={this} id='map' ref={this.mapRef}/>
     </div>
   )
  }
}

export default App
