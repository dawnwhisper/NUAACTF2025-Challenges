/**
 * Created by wgw on 2015/3/16.
 */
/*属性可以不事先声明就使用？*/
/*变量的作用域？*/
function Circle(){
    createjs.Shape.call(this);

    this.setCircleType=function(type){
        this._circleType=type;
        switch (type){
            case Circle.TYPE_UNSELECTED:
                this.setColor("#cccccc");
                break;
            case Circle.TYPE_SELECTED:
                this.setColor("#ff9900");
                break;
            case Circle.TYPE_CAT:
                this.setColor("#00ff00");
                break;
            case Circle.TYPE_CAT_SURROUNDED:
                this.setColor("#ff0000");
                break;
        }
    }
    this.setColor=function(colorString){
        this.graphics.beginFill(colorString);
        //this.graphics.beginStroke(colorString);
        this.graphics.drawCircle(0,0,25);
        this.graphics.endFill();
    }
    this.getCircleType=function(){
        return this._circleType;
    }
    this.setCircleType(Circle.TYPE_UNSELECTED);

}
Circle.prototype=new createjs.Shape();
Circle.TYPE_UNSELECTED=0;
Circle.TYPE_SELECTED=1;
Circle.TYPE_CAT=-1;
Circle.TYPE_CAT_SURROUNDED=-2;