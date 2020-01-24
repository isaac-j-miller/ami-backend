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
            if(this.props.parrent.sideBarRef.state.activeOverlay!='RGB'){
                this.setState({url:this.props.parent.mapRef.current.state.activeOverlay.scale});
            }
        }
    }
    render(){
        if(this.state.url!==null){
            return <img src={this.state.url} alt='color scale' className={this.state.visible? 'color-scale': 'hidden-color-scale'}/>
        }
        else{
            return <div/>
        }
        
        
    }
}