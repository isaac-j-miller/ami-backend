import React, {Component} from 'react';
import DeckGL, {BitmapLayer} from 'deck.gl';
import ReactMapGL,{Marker} from 'react-map-gl'
import Pin from './Pin'
import axios from 'axios';
import backend from '../globals'
const TOKEN = 'pk.eyJ1IjoiaXNhYWNqbWlsbGVyIiwiYSI6ImNrMTZ6NnBqdjFiM3czcHRrb3ZtbTZsajYifQ.3tv9y_9KCHST0M5NaDj4Zg'; // Set your mapbox token here
const mapStyle = {
    mapboxDefault:'mapbox://styles/isaacjmiller/ck5lue3zg14c21ilphvbyq25t',
    openMapTile: 'https://api.maptiler.com/maps/hybrid/style.json?key=gQCnC8ZYWGvM8WdKZNmW'
  }

  
export default class Map extends Component {
  constructor(props){
    super(props);
    this.state = {
      viewport: {
        longitude: -79.4989,
        latitude: 37.9307,
        zoom: 15,
        offset: 0
      },
      activeOverlay: null,
      displayPins: true,
      pinsLoaded: false,
      markers: [],
      pinReady:true,
      scaleUrl: null
    }
    this.deckRef=React.createRef();
    this._onClickMethod=this._onClickMethod.bind(this);
    this.startPinTimer=this.startPinTimer.bind(this);
    this.renderPins=this.renderPins.bind(this);
    this.updateWindowDimensions=this.updateWindowDimensions.bind(this);
    
  }
  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
    
  }

  updateWindowDimensions() {
    this.setState({ height: window.innerHeight-40+'px',width:window.innerWidth+'px' });
  }
  startPinTimer(){
    console.log('pinready should be false')
    this.setState({pinReady:false})
    setTimeout(function(){this.setState({pinReady:true})}.bind(this),500);
  }
  _onViewportChange = viewport => {
    this.setState({viewport});
  }
  
  _onClickMethod(map,e){
    e.preventDefault();
    console.log(e.lngLat)
    let lng = e.lngLat[0];
    let lat = e.lngLat[1];
    let id;
    if(this.state.pinReady & this.state.displayPins){
      axios.get(`${backend.value}/notes/req/get_next_id`)
      .then(res =>{
        id = res.data.id;
        let user = this.props.parent.state.user;
        let field = this.props.parent.state.activeField;
        let today = new Date();
        let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        let dateTime = date+' '+time;
        axios.get(`${backend.value}/notes/req/update_add_note/?id=${id}&user=${user}&field=${field}&date=${dateTime}&latitude=${lat}&longitude=${lng}&value=${''}`)
        .then( res =>{
          this.setState({pinsLoaded:false})
          
        })
      })
    }
    console.log(e.target)
  }
  getLayer(){
    const layer = new BitmapLayer({
      id: 'bitmap-layer',
      bounds: this.state.activeOverlay.bounds,
      image: this.state.activeOverlay.image,
      transparentColor: [0,0,0,0]
    });
    return (layer);
  }
  getPins(){
    if(this.props.parent.state.user!==''){
      axios.get(`${backend.value}/notes/req/get_notes/?user=${this.props.parent.state.user}&field=${this.props.parent.state.activeField}`)
      .then(res =>{
        const info = res.data;
        let notes = [];
        let currentMarkers = this.state.markers;

        info.notes.forEach(function(marker){
          notes.push(marker);
          let hidden=true
          for(let i = 0; i<currentMarkers.length; i++){
            if(currentMarkers[i].id===marker.id){
              hidden=currentMarkers[i].hidden;
            }
          }
          notes[notes.length-1].hidden=hidden;
        })
        this.setState({markers:notes});
        //console.log(this.state.markers)
      }
      )};
    this.setState({pinsLoaded:true})
  }
  renderPins(){
    let t = this;
    if(this.state.displayPins){
      if(!this.state.pinsLoaded){
        this.getPins();
      }
      return(this.state.markers.map(function(element){
        //console.log(element)
        
        return(
        <Marker 
        
          key={element.id}
          latitude={element.latitude}
          longitude={element.longitude}
        >
          
          <Pin height='20' width='auto' key={element.id}
          {...element} parent={t}
        /></Marker>
        )})
      )
      }
    else{
      return <div/>
    }

  }
  render() {
    
    if( this.state.activeOverlay!=null){
      //console.log('real activeOverlay')
      return (
        <ReactMapGL
        {...this.state.viewport}
        width={this.state.width}
        height={this.state.height}
        onViewportChange={this._onViewportChange}
        mapStyle = {mapStyle.mapboxDefault}
        mapboxApiAccessToken={TOKEN}
        onClick = {(e)=>this._onClickMethod(ReactMapGL, e)}
        touchRotate = {true}
      >
        <DeckGL ref={this.deckRef}
        viewState={this.state.viewport}
        layers={[this.getLayer()]}
        />
        
        {this.renderPins()}
      </ReactMapGL>
        )
      }
  else{
    //console.log('null activeOverlay')
    return(
      
      <ReactMapGL
        {...this.state.viewport}
        width={this.state.width}
        height={this.state.height}
        onViewportChange={this._onViewportChange}
        mapStyle = {mapStyle.mapboxDefault}
        mapboxApiAccessToken={TOKEN}
        onClick = {(e)=>this._onClickMethod(ReactMapGL, e)}
        touchRotate = {true}
      >
        {this.renderPins()}
      </ReactMapGL>
  
        )
      }
  }
}