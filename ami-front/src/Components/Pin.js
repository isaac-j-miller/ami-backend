import React, {Component} from 'react';
import PinPopUp from './PinPopUp'
import styles from './Style/PinStyle.css'

const ICON = `M20.2,15.7L20.2,15.7c1.1-1.6,1.8-3.6,1.8-5.7c0-5.6-4.5-10-10-10S2,4.5,2,10c0,2,0.6,3.9,1.6,5.4c0,0.1,0.1,0.2,0.2,0.3
  c0,0,0.1,0.1,0.1,0.2c0.2,0.3,0.4,0.6,0.7,0.9c2.6,3.1,7.4,7.6,7.4,7.6s4.8-4.5,7.4-7.5c0.2-0.3,0.5-0.6,0.7-0.9
  C20.1,15.8,20.2,15.8,20.2,15.7z`;

const pinStyle = {
  fill: '#d00',
  stroke: 'none'
};

export default class Pin extends Component{
    constructor(props){
        super(props);
        this.state = {
            id:this.props.id,
            user:this.props.user,
            field:this.props.field,
            date:this.props.date,
            latitude:this.props.latitude,
            longitude:this.props.longitude,
            value:this.props.value,
            hidden:false
        }
        this.popUpRef=React.createRef();
        this.onClick=this.onClick.bind(this)
    }
    _onViewportChange = viewport => {
        this.setState({viewport});
      }
    onClick(){
        console.log('marker has been clicked');
        this.popUpRef.current.setState({visible: !this.popUpRef.current.state.visible});
    }
    componentDidMount(){
        console.log('marker has mounted')
    }
    getClass(){
        if(this.state.hidden){
            return 'hidden'
        }
        else{
            return 'visible'
        }
    }
    render(){
        return(
           
            <div>
            <svg viewBox="0 0 24 24" className={`pin-logo ${this.getClass()}`} onClick = {this.onClick}>
                <path d={ICON} />
            </svg>
                <PinPopUp ref={this.popUpRef} {...this.state} parent={this} grandparent={this.props.parent}/>
            </div>
            
        )
    }
}