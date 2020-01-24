import React, {Component} from 'react';
import axios from 'axios'
import styles from '../Components/Style/SideBarStyle.css'
import backend from '../globals'
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
            overlayInfo: {default:{long:'default',summary:'default'}},
            activeOverlay:'default',
            indexInfoHidden:true,
            hidden:true,
            displayPinText:'Hide Pins',
            reqOverlayClass:'',
            remOverlayClass:'hidden-button '
        }
        
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleDateChange = this.handleDateChange.bind(this);
        this.handleOverlayChange = this.handleOverlayChange.bind(this);
        this.handleRequestOverlay = this.handleRequestOverlay.bind(this);
        this.handleRemoveOverlay = this.handleRemoveOverlay.bind(this);
        this.handleTogglePins=this.handleTogglePins.bind(this);
        this.setNewViewPort=this.setNewViewPort.bind(this);
        this.getIndexInfoClass=this.getIndexInfoClass.bind(this);
        this.handleOpenUpload=this.handleOpenUpload.bind(this);
        this.fieldsRef=React.createRef();
        this.datesRef=React.createRef();
        this.overlaysRef=React.createRef();
    }
    handleFieldChange(event){
        event.preventDefault();
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
    handleOpenUpload(){
        this.props.parent.uploaderRef.current.setState({visible:true});
    }
    handleTogglePins(){
        this.props.parent.mapRef.current.setState({displayPins:!this.props.parent.mapRef.current.state.displayPins});
        //this.props.parent.mapRef.current.setState({pinsLoaded:false});
        if(!this.props.parent.mapRef.current.state.displayPins){
            
            this.setState({displayPinText:'Hide Pins'})
        }
        else{
            this.setState({displayPinText:'Show Pins'})
        }
    
    }
    handleDateChange(event){
        this.props.parent.setState({activeDate:event.target.value});
        this.setState({activeDate:event.target.value});
        if(this.props.parent.mapRef.current.state.activeOverlay){
            this.handleRequestOverlay(undefined, null, event.target.value);
        }
    }
    handleOverlayChange(event){
        this.props.parent.setState({activeOverlay:event.target.value});
        this.setState({activeOverlay:event.target.value});
        this.handleRequestOverlay(event, event.target.value);
    }
    handleRemoveOverlay(event){
        this.props.parent.mapRef.current.setState({activeOverlay:null})
        this.props.parent.scaleRef.current.setState({url:null});
        //this.forceUpdate();
        this.setState({indexInfoHidden:true});
        this.setState({remOverlayClass:'hidden-button '})
        this.setState({reqOverlayClass:''})
    }
    componentDidMount(){
        this.getFields();
        
    }
    getDates(){
        axios.get(`${backend.value}/stacks/req/request_dates/?user=${this.state.user}&field=${this.state.activeField}`)
        .then(res =>{
            const info = res.data;
            this.setState({dates:info.dates});
            for(let i = 0; i<this.state.dates.length;i++){
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
        for(let i = 0; i<this.state.fields.length;i++){
            this.state.fieldsArray.push({key: i, value: this.state.fields[i]});
        }
        this.props.parent.setState({activeField:this.state.fields[0]});
        this.setState({activeField:this.state.fields[0]});
        try{
            this.props.parent.uploaderRef.current.setState({fieldsArray: this.state.fieldsArray});
        }
        catch(err){
            //console.warn(err);
        }
        this.forceUpdate();
    }
    getOverlays(){
        for(let i = 0; i<this.state.overlays.length;i++){
            this.state.overlaysArray.push({key: i, value: this.state.overlays[i]});
        }
        this.props.parent.setState({activeOverlay:this.state.overlays[0]});
        this.setState({activeOverlay:this.state.overlays[0]});
        
        this.forceUpdate();
    }
    handleRequestOverlay(event, newOverlay=null, newDate=null, newField=null){
        let overlay = this.state.activeOverlay;
        let date = this.state.activeDate;
        let field = this.state.activeField;
        if (newOverlay!==null){
            overlay=newOverlay;
        }
        if (newDate!==null){
            date=newDate;
        }
        if (newField!==null){
            field=newField;
        }
        //console.log(this.state)
        axios.get(`${backend.value}/overlays/req/request_overlay/?user=${this.state.user}&field=${field}&date=${date}&index_name=${overlay}`)
        .then(res =>{
            const info = res.data;
            if(info.available){
                this.props.parent.mapRef.current.setState({activeOverlay:{
                    image: info.png,
                    bounds: info.bounds,
                    scale: info.scale
                }});
                console.log(info);
                this.props.parent.scaleRef.current.setState({url:info.scale});
                //this.props.parent.mapRef.current.forceUpdate();
                this.setState({indexInfoHidden:false});
                this.setState({reqOverlayClass:'hidden-button '})
                this.setState({remOverlayClass:''})
                
                this.props.parent.scaleRef.current.setState({visible:!(this.state.activeOverlay=='RGB')});
            
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
    getReqOverlayClass(){
        try{
            if (this.props.parent.mapRef.current.state.activeOverlay!==null){
                return 'hidden-button'
            }
            else{
                return ''
            } 
        }
        catch(err){
            //console.warn(err);
        }
    }
    getRemOverlayClass(){
        try{
            if (this.props.parent.mapRef.current.state.activeOverlay===null){
                return 'hidden-button '
            }
            else{
                return ''
            } 
        }
        catch(err){
            //console.warn(err);
            return 'hidden-button '
        }
    }
    getInfoHeader(){
        try{
            return `Information about ${this.state.activeOverlay}: ${this.state.overlayInfo[this.state.activeOverlay].long}`
        }
        catch(err){

        }
    }
    getInfoBody(){
        try{
            return this.state.overlayInfo[this.state.activeOverlay].summary
        }
        catch(err){

        }
    }
    render(){
        //console.log(this.state);
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
                    <select className={this.getSubItemClass()} onChange={this.handleDateChange}>
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
                <button className={this.state.reqOverlayClass+this.getSubItemClass()+' sidebar-button'} onClick={this.handleRequestOverlay}>Request Overlay</button>
                <button className={this.state.remOverlayClass+this.getSubItemClass()+' sidebar-button'} onClick={this.handleRemoveOverlay}>Remove Overlay</button>
                <button className={this.getSubItemClass()+' sidebar-button'} onClick={this.handleTogglePins}>{this.state.displayPinText}</button>
                <button className={this.getSubItemClass()+' sidebar-button'} onClick={this.handleOpenUpload}>Upload New Flight</button>
                <div className={`indexInfo-wrapper ${this.getIndexInfoClass()}`}>
                    <h1 className='sidebar-header'>
                        {this.getInfoHeader()}
                    </h1>
                    <p className='sidebar-p'>
                        {this.getInfoBody()}
                    </p>
                </div>
                
            </div>
        )
    }
}

export default SideBar