import React, {Component} from 'react';
import axios from 'axios'

class SideBar extends Component{
    constructor(props){
        super(props)
        this.state = {user:'',fields:[], activeField:'', fieldsArray:[], dates: [], activeDate:'',datesArray: [], overlaysArray: [], activeOverlay:''}
        
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleDateChange = this.handleDateChange.bind(this);
        this.handleOverlayChange = this.handleOverlayChange.bind(this);
        this.handleRequestOverlay = this.handleRequestOverlay.bind(this);
        this.fieldsRef=React.createRef();
        this.datesRef=React.createRef();
        this.overlaysRef=React.createRef();
        console.log(this.props);
    }
    handleFieldChange(event){
        event.preventDefault();
        //TODO: send the activeField info up to parent
        console.log('handling field change')
        console.log(event.target.value);
        this.props.parent.setState({activeField:event.target.value});
        this.setState({activeField:event.target.value});
        
    }
    handleDateChange(event){
        this.props.parent.setState({activeDate:event.target.value});
        this.setState({activeDate:event.target.value});
    }
    handleOverlayChange(event){
        this.props.parent.setState({activeOverlay:event.target.value});
        this.setState({activeOverlay:event.target.value});
    }
    componentDidMount(){
        
        console.log(this.state);
        this.getFields();
        
    }
    getDates(){
        axios.get(`http://localhost:8000/stacks/req/request_dates/?user=${this.state.user}&field=${this.state.activeField}`)
        .then(res =>{
            const info = res.data;
            this.state.dates=info.dates;
            console.log('datesrequest:')
            console.log(info);
            console.log(info.length);
            for(let i = 0; i<this.state.dates.length;i++){
                console.log(i);
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
        console.log(this.state);
        for(let i = 0; i<this.state.fields.length;i++){
            this.state.fieldsArray.push({key: i, value: this.state.fields[i]});
        }
        console.log(this.state.fieldsArray);
        this.props.parent.setState({activeField:this.state.fields[0]});
        this.setState({activeField:this.state.fields[0]});
        
        this.forceUpdate();
    }
    getOverlays(){
        console.log('getting overlays')
        console.log(this.state);
        for(let i = 0; i<this.state.overlays.length;i++){
            this.state.overlaysArray.push({key: i, value: this.state.overlays[i]});
        }
        console.log(this.state.fieldsArray);
        this.props.parent.setState({activeOverlay:this.state.overlays[0]});
        this.setState({activeOverlay:this.state.overlays[0]});
        
        this.forceUpdate();
    }
    handleRequestOverlay(event){

    }
    render(){
        return (
            <div class="sidebar">
                <label>Select Field
                    <select onChange={this.handleFieldChange}>
                        {this.state.fieldsArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <label>Select Date
                    <select onChange={this.handleFieldChange}>
                        {this.state.datesArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <label>Select Index
                    <select onChange={this.handleOverlayChange}>
                        {this.state.overlaysArray.map(function(element){
                            return(
                            <option key={element.key} value={element.value}>{element.value}</option>
                        )})}
                    </select>
                </label>
                <label>
                    <button onClick={this.handleRequestOverlay}>Request Overlay</button>
                </label>
                
            </div>
        )
    }
}

export default SideBar