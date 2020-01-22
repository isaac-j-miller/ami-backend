import React, {Component} from 'react';
import axios from 'axios'
import styles from '../Components/Style/SideBarStyle.css'
class SideBar extends Component{
    constructor(props){
        super(props)
        this.state = {
            user:'',
            fields:[], 
            activeField:'', 
            fieldsArray:[], 
            dates: [], 
            activeDate:'',
            datesArray: [], 
            overlaysArray: [], 
            activeOverlay:'',
            indexInfoHidden:true,
            hidden:true
        }
        
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleDateChange = this.handleDateChange.bind(this);
        this.handleOverlayChange = this.handleOverlayChange.bind(this);
        this.handleRequestOverlay = this.handleRequestOverlay.bind(this);
        this.handleRemoveOverlay = this.handleRemoveOverlay.bind(this);
        this.handleTogglePins=this.handleTogglePins.bind(this);
        this.setNewViewPort=this.setNewViewPort.bind(this);
        this.getIndexInfoClass=this.getIndexInfoClass.bind(this);
        //this.getSubItemClass=this.getSubItemClass.bind(this);
        this.fieldsRef=React.createRef();
        this.datesRef=React.createRef();
        this.overlaysRef=React.createRef();
        
        //console.log(this.props);
    }
    handleFieldChange(event){
        event.preventDefault();
        //TODO: send the activeField info up to parent
        //console.log('handling field change')
        //console.log(event.target.value);
        this.props.parent.setState({activeField:event.target.value});
        this.setState({activeField:event.target.value});
        this.setNewViewPort()
    }
    setNewViewPort(){
        if(this.props.parent.state.origins!==null & this.state.activeField!==''){
            let lat = this.props.parent.state.origins[this.state.activeField].latitude;
            let lon = this.props.parent.state.origins[this.state.activeField].longitude;
            console.log(`lat: ${lat}, lon: ${lon}`)
            this.props.parent.mapRef.current.setState({viewport:{
                latitude: lat,
                longitude: lon,
                zoom: 15,
                offset: 0
            }});
            
        }
    }
    handleTogglePins(){
        this.props.parent.mapRef.current.setState({displayPins:!this.props.parent.mapRef.current.state.displayPins});
        if(!this.props.parent.mapRef.current.state.displayPins){
            this.props.parent.mapRef.current.setState({pinsLoaded:false});
        }
    }
    handleDateChange(event){
        this.props.parent.setState({activeDate:event.target.value});
        this.setState({activeDate:event.target.value});
    }
    handleOverlayChange(event){
        this.props.parent.setState({activeOverlay:event.target.value});
        this.setState({activeOverlay:event.target.value});
    }
    handleRemoveOverlay(event){
        this.props.parent.mapRef.current.setState({activeOverlay:null})
        this.props.parent.scaleRef.current.setState({url:null});
        this.setState({indexInfoHidden:true});
    }
    componentDidMount(){
        
        //console.log(this.state);
        this.getFields();
        
    }
    getDates(){
        axios.get(`http://3.219.163.17:8000/stacks/req/request_dates/?user=${this.state.user}&field=${this.state.activeField}`)
        .then(res =>{
            const info = res.data;
            this.setState({dates:info.dates});
            //console.log('datesrequest:')
            //console.log(info);
            //console.log(info.length);
            for(let i = 0; i<this.state.dates.length;i++){
                //console.log(i);
                this.state.datesArray.push({key: i, value: this.state.dates[i]});
            }
            this.props.parent.setState({activeDate:this.state.dates[0]});
            this.setState({activeDate:this.state.dates[0]});
            this.forceUpdate();
        })
        .catch(function(error){
            console.warn(error);
        });
        
    }
    getFields(){
        //console.log(this.state);
        for(let i = 0; i<this.state.fields.length;i++){
            this.state.fieldsArray.push({key: i, value: this.state.fields[i]});
        }
        //console.log(this.state.fieldsArray);
        this.props.parent.setState({activeField:this.state.fields[0]});
        this.setState({activeField:this.state.fields[0]});
        
        this.forceUpdate();
    }
    getOverlays(){
        //console.log('getting overlays')
        //console.log(this.state);
        for(let i = 0; i<this.state.overlays.length;i++){
            this.state.overlaysArray.push({key: i, value: this.state.overlays[i]});
        }
        //console.log(this.state.fieldsArray);
        this.props.parent.setState({activeOverlay:this.state.overlays[0]});
        this.setState({activeOverlay:this.state.overlays[0]});
        
        this.forceUpdate();
    }
    handleRequestOverlay(event){
        axios.get(`http://3.219.163.17:8000/overlays/req/request_overlay/?user=${this.state.user}&field=${this.state.activeField}&date=${this.state.activeDate}&index_name=${this.state.activeOverlay}`)
        .then(res =>{
            const info = res.data;
            //TODO: extract necessary data and send it to the map
            if(info.available){
                this.props.parent.mapRef.current.setState({activeOverlay:{
                    image: info.png,
                    bounds: info.bounds,
                    scale: info.scale
                }});
                this.props.parent.scaleRef.current.setState({url:info.scale});
                this.props.parent.mapRef.current.forceUpdate();
                this.setState({indexInfoHidden:false});
                //console.log('forced update on map')
            }

            
        })
        .catch(function(error){
            console.warn(error);
        });
    }
    getClass(){
        if(this.state.hidden){
            return 'sidebar-hidden';
        }
        else{
            return 'sidebar-visible';
        }
    }
    getSubItemClass(){
        if(this.state.hidden){
            return 'subitem-hidden';
        }
        else{
            return 'subitem-visible';
        }
    }
    getIndexInfoClass(){
        if(this.state.indexInfoHidden){
            return 'hidden'
        }
        else{
            return ''
        }
    }
    render(){
        return (
            <div className={this.getClass()}>
                <label className={this.getSubItemClass()}>Select Field
                    <select className={this.getSubItemClass()} onChange={this.handleFieldChange}>
                        {this.state.fieldsArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <label className={this.getSubItemClass()}>Select Date
                    <select className={this.getSubItemClass()} onChange={this.handleFieldChange}>
                        {this.state.datesArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <label className={this.getSubItemClass()} >Select Index
                    <select className={this.getSubItemClass()} onChange={this.handleOverlayChange}>
                        {this.state.overlaysArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <button className={this.getSubItemClass()+' sidebar-button'} onClick={this.handleRequestOverlay}>Request Overlay</button>
                <button className={this.getSubItemClass()+' sidebar-button'} onClick={this.handleRemoveOverlay}>Remove Overlay</button>
                <button className={this.getSubItemClass()+' sidebar-button'} onClick={this.handleTogglePins}>Toggle Display Pins</button>
                <div className={`indexInfo-wrapper ${this.getIndexInfoClass()}`}>
                    <h1 className='sidebar-header'>
                        Information about {this.state.activeOverlay.toUpperCase()}
                    </h1>
                    <p className='sidebar-p'>
                        Lorem Ipsum blah blah blah about the index, will be replaced later with actual stuff
                    </p>
                </div>
            </div>
        )
    }
}

export default SideBar