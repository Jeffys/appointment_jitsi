# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID
from . import controllers
from . import models


def reset_mail_templates(env, default_values):
    template_model = env['mail.template']    
    for template_name, values in default_values.items():
        template_ids = template_model.search([('name', '=', template_name)])
        if template_ids:
            template_ids.write(values)

def _uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Define the default values for the template [Calendar: Event Update]
    default_calendar_event_update = {
        'Calendar: Event Update': {
            'subject': 'Calendar: Event Update',
            'body_html': """
                <div>
                    <t t-set="colors" t-value="{'needsAction': 'grey', 'accepted': 'green', 'tentative': '#FFFF00', 'declined': 'red'}" />
                    <t t-set="is_online" t-value="'appointment_type_id' in object and object.appointment_type_id" />
                    <t t-set="target_responsible" t-value="object.partner_id == object.partner_id" />
                    <t t-set="target_customer" t-value="object.partner_id == customer" />
                    <t t-set="recurrent" t-value="object.recurrence_id and not ctx.get('calendar_template_ignore_recurrence')" />
                    <t t-set="mail_tz" t-value="object._get_mail_tz() or ctx.get('mail_tz')" />
                    <div>
                        <table border="0" cellpadding="0" cellspacing="0">
                            <tr>
                                <td width="130px;" style="min-width: 130px;">
                                    <div style="border-top-start-radius: 3px; border-top-end-radius: 3px; font-size: 12px; border-collapse: separate; text-align: center; font-weight: bold; color: #ffffff; min-height: 18px; background-color: #875A7B; border: 1px solid #875A7B;">
                                        <t t-out="format_datetime(dt=object.start, tz=mail_tz if not object.allday else None, dt_format='EEEE', lang_code=object.env.lang) "></t>
                                    </div>
                                    <div style="font-size: 48px; min-height: auto; font-weight: bold; text-align: center; color: #5F5F5F; background-color: #F8F8F8; border: 1px solid #875A7B;">
                                        <t t-out="format_datetime(dt=object.start, tz=mail_tz if not object.allday else None, dt_format='d', lang_code=object.env.lang)"></t>
                                    </div>
                                    <div style='font-size: 12px; text-align: center; font-weight: bold; color: #ffffff; background-color: #875A7B;'>
                                        <t t-out="format_datetime(dt=object.start, tz=mail_tz if not object.allday else None, dt_format='MMMM y', lang_code=object.env.lang)"></t>
                                    </div>
                                    <div style="border-collapse: separate; color: #5F5F5F; text-align: center; font-size: 12px; border-bottom-end-radius: 3px; font-weight: bold; border: 1px solid #875A7B; border-bottom-start-radius: 3px;">
                                        <t t-if="not object.allday">
                                            <div>
                                                <t t-out="format_time(time=object.start, tz=mail_tz, time_format='short', lang_code=object.env.lang)"></t>
                                            </div>
                                            <t t-if="mail_tz">
                                                <div style="font-size: 10px; font-weight: normal">
                                                    (<t t-out="mail_tz"></t>)
                                                </div>
                                            </t>
                                        </t>
                                    </div>
                                </td>
                                <td width="20px;"/>
                                <td style="padding-top: 5px;">
                                    <p>
                                        <strong>Details of the event</strong>
                                    </p>
                                    <ul>
                                        <t t-if="not is_html_empty(object.description)">
                                            <li>Description:
                                            <t t-out="object.description">Internal meeting for discussion for new pricing for product and services.</t></li>
                                        </t>
                                        <li>
                                            How to Join:
                                            <t t-if="object.get_base_url() in object.videocall_location"> Join with Odoo Discuss</t>
                                            <t t-else=""> Join at</t><br/>
                                            <a t-att-href="object.videocall_location" target="_blank" t-out="object.videocall_location or ''">www.mycompany.com/calendar/join_videocall/xyz</a>
                                        </li>

                                        <t t-if="object.location">
                                            <li>Location: <t t-out="object.location or ''"></t>
                                                (<a target="_blank"
                                                    t-attf-href="http://maps.google.com/maps?oi=map&amp;q={{object.location}}">View Map</a>)
                                            </li>
                                        </t>
                                        <t t-if="recurrent">
                                            <li>When: <t t-out="object.recurrence_id.name or ''"></t></li>
                                        </t>
                                        <t t-if="not object.allday and object.duration">
                                            <li>Duration:
                                                <t t-out="('%dH%02d' % (object.duration,round(object.duration*60)%60))"></t>
                                            </li>
                                        </t>
                                    </ul>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="user_input">
                        <hr/>
                        <p placeholder="Enter your message here"><br/></p>

                    </div>
                </div>
            """,
        },
        # Add more templates if needed
    }
    
    # Define the default values for the template [Calendar: Event Update]
    reset_mail_templates(env, default_calendar_event_update)

    # Define the default values for the template [Appointment: Appointment Booked]
    default_calendar_appointment_booked = {
        'Appointment: Appointment Booked': {
            'subject': 'Appointment: Appointment Booked',
            'body_html': """                 
                <div>
                    <t t-set="colors" t-value="{'needsAction': 'grey', 'accepted': 'green', 'tentative': '#FFFF00', 'declined': 'red'}" />
                    <t t-set="recurrent" t-value="object.recurrence_id and not ctx.get('calendar_template_ignore_recurrence')" />
                    <t t-set="mail_tz" t-value="object._get_mail_tz() or ctx.get('mail_tz')" />

                    <p>
                        Appointment booked for <t t-out="object.appointment_type_id.name or 'Technical Demo'"/>
                        <t t-if="object.appointment_type_id.category != 'custom'">
                            with <t t-out="object.partner_id.name or 'Brandon Freeman'"/>
                        </t>.
                    </p>

                    <div style="text-align: center; padding: 16px 0px 16px 0px;">
                        <a t-attf-href="/calendar/meeting/join?token={{ object.access_token }}"
                           style="padding: 5px 10px; color: #FFFFFF; text-decoration: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius: 3px">
                            Join</a>
                        <a t-attf-href="/web?#id={{ object.id }}&amp;view_type=form&amp;model=calendar.event"
                           style="padding: 5px 10px; color: #FFFFFF; text-decoration: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius: 3px">
                            View</a>
                    </div>

                    <table border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            <td width="130px;" style="min-width: 130px;">
                                <div style="border-top-start-radius: 3px; border-top-end-radius: 3px; font-size: 12px; border-collapse: separate; text-align: center; font-weight: bold; color: #ffffff; min-height: 18px; background-color: #875A7B; border: 1px solid #875A7B;">
                                    <t t-out="format_datetime(dt=object.start, tz=mail_tz if not object.allday else None, dt_format='EEEE', lang_code=object.env.lang) or 'Wednesday'"/>
                                </div>
                                <div style="font-size: 48px; min-height: auto; font-weight: bold; text-align: center; color: #5F5F5F; background-color: #F8F8F8; border: 1px solid #875A7B;">
                                    <t t-out="str(object.start.day) or '1'"/>
                                </div>
                                <div style='font-size: 12px; text-align: center; font-weight: bold; color: #ffffff; background-color: #875A7B;'>
                                    <t t-out="format_datetime(dt=object.start, tz=mail_tz if not object.allday else None, dt_format='MMMM y', lang_code=object.env.lang) or 'January 2020'"/>
                                </div>
                                <div style="border-collapse: separate; color: #5F5F5F; text-align: center; font-size: 12px; border-bottom-end-radius: 3px; font-weight: bold; border: 1px solid #875A7B; border-bottom-start-radius: 3px;">
                                    <t t-if="not object.allday">
                                        <div>
                                            <t t-out="format_time(time=object.start, tz=mail_tz, time_format='short', lang_code=object.env.lang) or '8:00'"/>
                                        </div>
                                        <t t-if="mail_tz">
                                            <div style="font-size: 10px; font-weight: normal;">
                                                (<t t-out="mail_tz"/>)
                                            </div>
                                        </t>
                                    </t>
                                </div>
                            </td>
                            <td width="20px;"/>
                            <td style="padding-top: 5px;">
                                <p><strong>Details of the event</strong></p>
                                <ul>
                                    <li t-if="object.location">
                                        Location: <t t-out="object.location or 'Bruxelles'"/>
                                        (<a target="_blank" t-attf-href="http://maps.google.com/maps?oi=map&amp;q={{ object.location }}">View Map</a>)
                                    </li>
                                    <li t-if="recurrent">
                                        When: <t t-out="object.recurrence_id.name or 'Every 1 Weeks, for 3 events'"/>
                                    </li>
                                    <li t-if="not object.allday and object.duration">
                                        Duration: <t t-out="'%dH%02d' % (object.duration, round(object.duration * 60) % 60) or '0H30'"/>
                                    </li>
                                    <li>
                                        Attendees
                                        <ul>
                                            <li t-foreach="object.attendee_ids" t-as="attendee">
                                                <div t-attf-style="display: inline-block; border-radius: 50%; width: 10px; height: 10px; background: {{ colors.get(attendee.state) or 'white' }};"> </div>
                                                <t t-if="attendee.common_name">
                                                    <span style="margin-left: 5px;" t-out="attendee.common_name or 'Mitchell Admin'"/>
                                                </t>
                                                <t t-else="">
                                                    <span style="margin-left: 5px;">You</span>
                                                </t>
                                            </li>
                                        </ul>
                                    </li>
                                    <li t-if="object.videocall_location">
                                        How to Join:
                                        <t t-if="object.get_base_url() in object.videocall_location"> Join with Odoo Discuss</t>
                                        <t t-else=""> Join at</t><br/>
                                        <a t-attf-href="{{ object.videocall_location }}" target="_blank" t-out="object.videocall_location or ''">www.mycompany.com/calendar/join_videocall/xyz</a>
                                    </li>
                                    <li t-if="not is_html_empty(object.description)">
                                        Description of the event:
                                        <t t-out="object.description"/>
                                    </li>
                                </ul>
                            </td>
                        </tr>
                    </table>
                </div>
            """,
        },
        # Add more templates if needed
    }
    
   # Define the default values for the template [Appointment: Appointment Booked]
    reset_mail_templates(env, default_calendar_appointment_booked)      

    
        

    
            