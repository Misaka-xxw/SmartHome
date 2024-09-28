export default {
 
    memberObj:{
 
        name:[],
 
    },
 
    setMemberObj(data){
 
        this.memberObj = Object.assign({},this.memberObj,data)
 
    }
 
}