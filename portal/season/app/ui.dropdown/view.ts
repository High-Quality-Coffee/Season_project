import { OnInit } from '@angular/core';
import { Input } from '@angular/core';
import { ContentChild, TemplateRef } from '@angular/core';
import { HostListener } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() menuStyle: any = {};

    constructor(public service: Service) { }

    public isOpen: boolean = false;
    public onToggle: any = false;

    @ContentChild('button') button: TemplateRef<any>;
    @ContentChild('menu') menu: TemplateRef<any>;

    public async ngOnInit() { }

    public async toggle(stat: any = null) {
        this.onToggle = true;
        if (stat !== null) {
            this.isOpen = stat;
        } else {
            this.isOpen = !this.isOpen;
        }
        await this.service.render();
        // $event.stopPropagation();
    }

    @HostListener('document:click', ['$event.target'])
    public clickout() {
        if (this.onToggle) {
            this.onToggle = false;
            this.service.render();
            return;
        }

        if (this.isOpen)
            this.isOpen = false;
        this.service.render();
    }
}