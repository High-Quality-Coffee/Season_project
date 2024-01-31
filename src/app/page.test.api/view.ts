import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;
    public data: any = {
        name: ''
    }

    public async ngOnInit() {
    }

    public async test() {
        let user=JSON.parse(JSON.stringify(this.data));
        let { code, data } = await wiz.call("test",user)
        if(code != 200){
            return;
        }
        console.log(data);
        
    }

}