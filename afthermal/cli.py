import click

from . import ThermalPrinter, hw
from .text import Format
from .util import in_range


@click.group()
@click.option('-d', '--dev', default='/dev/ttyAMA0')
@click.pass_context
def main(ctx, dev):
    obj = {}
    ctx.obj = obj
    click.echo('Connecting to printer {}'.format(dev))
    obj['printer'] = ThermalPrinter.on_serial(dev)


@main.command()
@click.option('-h', '--heat-time', type=int,
              help='Do not calibrate heat_time, but set fixed at this value.')
@click.option('-i', '--interval', type=int,
              help='Do not calibrate interval, but set fixed at this value.')
@click.option('-d', '--max-dots', type=int,
              help='Do not calibrate max_dots, but set fixed at this value.')
@click.option('-y', '--yes', is_flag=True,
              help='Do not ask for confirmation before starting.')
@click.pass_obj
def calibrate(obj, interval, max_dots, heat_time, yes):
    def update_settings(cfg):
        cfg_format = ('heat_time: {0[heat_time]} us\n'
                      'interval: {0[interval]} us\n'
                      'max_dots: {0[max_dots]} dots\n')

        p.set_heat(**cfg)
        p.write(cfg_format.format(cfg))

    def try_settings(cfg, **kwargs):
        new_cfg = cfg.copy()
        new_cfg.update(kwargs)
        p.set_heat(**new_cfg)

    def read_user_int(name, validate):
        while True:
            val = click.prompt(name, type=int)
            if not validate(val):
                click.echo('Invalid {} value'.format(name))
            else:
                return val

    p = obj['printer']

    # Initial setup
    p.write("ready to calibrate\n\n\n")
    if not yes:
        click.echo('About to calibrate your printer. It should have printed '
                   '"ready to calibrate". Calibration will use up about ?? '
                   'cm of printer roll.')
        click.confirm("Continue?", abort=True, default=True)

    cfg = {
        'interval': interval if interval is not None else 20,
        'heat_time': heat_time if heat_time is not None else 800,
        'max_dots': max_dots if max_dots is not None else 64,
    }

    # fills a full line with some special chars at the beginning
    prefix = '#.$%_=ABCDE '
    test_str = Format(invert=True)(
        '{}{{:>{}s}}\n'.format(prefix, hw.CHARS_PER_LINE - len(prefix))
    )

    update_settings(cfg)

    # determine optimal heat
    if heat_time is None:
        click.echo('Determining heat. Please pick the lowest setting that '
                   'yields flawless black lines, do not worry about bad text '
                   'rendering.')
        for heat_time in range(200, 2551, 200):
            try_settings(cfg, heat_time=heat_time)
            p.write(test_str.format(
                ('heat_time: {:>4d} us'.format(heat_time))
            ))
        p.write('\n\n\n')

        cfg['heat_time'] = read_user_int('heat_time', in_range(30, 2550+1, 10))
        update_settings(cfg)

    # determine minimum interval
    if interval is None:
        click.echo('Determining interval. Please pick the lowest setting that '
                   'has crisp characters.')
        for interval in range(0, 300, 20):
            try_settings(cfg, interval=interval)
            p.write(test_str.format(
                ('interval: {:>4d} us'.format(interval))
            ))
        p.write('\n\n\n')

        cfg['interval'] = read_user_int('interval', in_range(0, 2550+1, 20))
        update_settings(cfg)

    # max_dots is last
    if max_dots is None:
        click.echo('Determining maximum speed (max dots). Please pick the '
                   'highest setting that still prints correctly.')
        for max_dots in range(8, 40*8, 16):
            try_settings(cfg, max_dots=max_dots)
            p.write(test_str.format(
                ('max_dots: {:>3d} dots'.format(max_dots))
            ))
        p.write('\n\n\n')

        cfg['max_dots'] = read_user_int('max_dots', in_range(8, 258*8, 8))
        update_settings(cfg)

    p.write('calibration finished\n\n\n\n')

    return
