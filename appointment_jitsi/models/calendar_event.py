# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models
import uuid


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    jitsi_link = fields.Text(string="Jitsi Link", store=True, copy=True, compute='_set_jitsi_link')

    # dummy method. this method is intercepted in the frontend and the value is set locally
    def set_jitsi_link(self):
        self._set_jitsi_link()

    def clear_jitsi_link(self):
        self.jitsi_link = False

    @api.depends('jitsi_link', 'access_token')
    def _set_jitsi_link(self):
        data = self.env['ir.config_parameter'].get_param('appointment_jitsi.is_jitsi')
        company_param_id = self.env['ir.config_parameter'].get_param('company_param')
        company_param = self.env['res.company'].sudo().search([('id', '=', company_param_id)], limit=1)
        company_param = company_param.name if company_param else 'My Company'
        if data:
            """ This method sets the jitsi_link to a jitsi route. """
            JITSI_ROUTE = 'https://meet.jit.si'
            company = company_param 
            for rec in self:
                if not rec.access_token:
                    rec.access_token = uuid.uuid4().hex
                rec.jitsi_link = f"{JITSI_ROUTE}/{company}/{company}-{rec.access_token}"
            return rec
        else:
            for rec in self:
                rec._set_discuss_videocall_location()
            return rec

    def action_join_video_call(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.jitsi_link if self.is_jitsi == True else self.videocall_location,
            'target': 'new'
        }

    @api.model
    def create(self, values):
        res = super(CalendarEvent, self).create(values)
        return res

    is_jitsi = fields.Boolean(
        string="Jitsi Integration", default=False,
    )

    @api.constrains("jitsi_link")
    def _compute_jitsi(self):
        data = self.env['ir.config_parameter'].get_param('appointment_jitsi.is_jitsi')
        for record in self:
            if data:
                record.is_jitsi = True
            else:
                record.is_jitsi = False


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_jitsi = fields.Boolean(
        string="Jitsi Integration", config_parameter='appointment_jitsi.is_jitsi', default=False
    )
    company_param = fields.Many2one(
        'res.company', 
        string="Company", 
        config_parameter='company_param',
        default=lambda self: self.env.company
    )