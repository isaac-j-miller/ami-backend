import React, {Component} from 'react'
import styles from './Style/ScaleStyle.css'
export default class Scale extends Component{
    constructor(props){
        super(props);
        this.state = {
            url:null,
            visible: true
        }
    }
    componentDidMount(){
        if(this.props.parent.mapRef.current!==null){
            if(this.props.parrent.sideBarRef.state.activeOverlay!=='RGB'){
                this.setState({url:this.props.parent.mapRef.current.state.activeOverlay.scale});
            }
        }
    }
    getTitle(){
        let index=this.props.parent.sideBarRef.current.state.activeOverlay;
        if (index==='RGB'){
            return '';
        }
        else if (index==='DSM'){
            return 'Elevation (ft)';
        }
        else if (index=='Thermal'){
            return `Temperature (${String.fromCharCode(176)}F)`;
        }
        else{
            return index;
        }

    }
    render(){
        if(this.state.url!==null){
            return (
                <div  className={this.state.visible? 'color-scale-div':'hidden-color-scale-div'}>
                    <img src={this.state.url} alt='color scale' className='color-scale'/>
                    <h1 className='scale-title'>{this.getTitle()}</h1>
                </div>
            )
        }
        else{
            return <div/>
        }
        
        
    }
}