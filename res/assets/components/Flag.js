import React from 'react';
import PropTypes from 'prop-types';
import {Button} from 'reactstrap';
import httpApi from '@pytsite/http-api';
import setupWidget from '@pytsite/widget';
import ReactDOM from "react-dom";
import './flag.scss';

export default class Flag extends React.Component {
    static propTypes = {
        className: PropTypes.string,
        counterFormat: PropTypes.string,
        count: PropTypes.number.isRequired,
        entity: PropTypes.string.isRequired,
        flaggedCaption: PropTypes.string,
        icon: PropTypes.string,
        isFlagged: PropTypes.bool.isRequired,
        link: PropTypes.string,
        linkDataTarget: PropTypes.string,
        linkDataToggle: PropTypes.string,
        linkTarget: PropTypes.string,
        unflaggedCaption: PropTypes.string,
        variant: PropTypes.string.isRequired,
    };

    static defaultProps = {
        counterFormat: '#',
        flaggedCaption: '',
        unflaggedCaption: '',
    };

    constructor(props) {
        super(props);

        this.state = {
            count: this.props.count,
            isFlagged: this.props.isFlagged,
        };

        this.onClick = this.onClick.bind(this);
    }

    onClick() {
        httpApi.patch(`flag/${this.props.variant}/${this.props.entity}`).then(r => {
            this.setState({
                count: r.count,
                isFlagged: r.status,
            });
        });
    }

    render() {
        const className = this.props.className + (this.state.isFlagged ? ' is-flagged' : '');
        const caption = this.state.isFlagged ? this.props.flaggedCaption : this.props.unflaggedCaption;
        const icon = this.props.icon ? <i className={this.props.icon}></i> : null;
        const counter = this.props.counterFormat && ' ' + this.props.counterFormat.replace('#', this.state.count);

        if (this.props.link) {
            return (
                <a href={this.props.link} target={this.props.linkTarget} className={`btn btn-link ${className}`.trim()} data-toggle={this.props.linkDataToggle} data-target={this.props.linkDataTarget}>
                    {icon}
                    {caption}
                    {counter}
                </a>
            )
        } else {
            return (
                <Button onClick={this.onClick} className={className.trim()} color={'link'}>
                    {icon}
                    {caption}
                    {counter}
                </Button>
            )
        }
    }
}

setupWidget('plugins.flag._widget.Flag', widget => {
    const c = <Flag
        className={widget.data('css')}
        count={widget.data('count')}
        counterFormat={widget.data('counterFormat')}
        entity={widget.data('entity')}
        icon={widget.data('icon')}
        isFlagged={widget.data('isFlagged') === 'True'}
        link={widget.data('link')}
        linkDataToggle={widget.data('linkDataToggle')}
        linkDataTarget={widget.data('linkDataTarget')}
        linkTarget={widget.data('linkTarget')}
        variant={widget.data('variant')}
    />;

    ReactDOM.render(c, widget.find('.widget-component')[0]);
});
