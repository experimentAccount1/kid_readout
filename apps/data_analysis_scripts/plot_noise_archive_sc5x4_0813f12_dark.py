import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import kid_readout.analysis.noise_archive

if not globals().has_key('arch'):
    arch = kid_readout.analysis.noise_archive.load_archive('/home/data/archive/StarCryo_5x4_0813f12.npy')
    arch['round_temp'] = np.round(arch.end_temp*1000/5)*5

#arch = arch[(arch.power_dbm > -114) & (arch.power_dbm <= -98)]
tmaxmk = 450.
tminmk = 100.
arch = arch[arch.end_temp < 0.35]
arch = arch[(arch.Q_i > 0) & (arch.Q_i < 1e6)] 
idxs = np.unique(arch['ridx'])

pset = arch[abs(arch.power_dbm +101.) < 1]
icolors = plt.cm.spectral(np.linspace(0.1,0.9,20))
fig = plt.figure()
ax = fig.add_subplot(111)
for idx in range(20):
    if idx in [9,13]:
        continue
    this = pset[pset.ridx == idx]
    this = this.sort(['end_temp'])
    ax.semilogy(this.end_temp*1000,this.noise_250_hz,'.-',lw=2,color=icolors[idx],label=('res #%d' % idx))
    ax.semilogy(this.end_temp*1000,this.noise_30_khz,'--',color=icolors[idx])
ax.legend(prop=dict(size='xx-small'))
ax.grid()
ax.set_xlim(tminmk,tmaxmk)
ax.set_ylim(1e-19,1e-14)
ax.set_title(('StarCryo_5x4_0813f12_Dark @ %.1f dBm' %(this.power_dbm.iat[0])),size='medium')
ax.set_xlabel('Temperature (mK)')
ax.set_ylabel('Noise Power (1/Hz)')
ax.text(0.95,0.1,"Solid = Device\nDashed = Amplifier",fontdict=dict(size='small'), ha='right',va='bottom',
            transform=ax.transAxes)
fig.savefig('/home/data/archive/StarCryo_5x4_0813f12_Dark_all.pdf',bbox_inches='tight')
    

for idx in range(20):
    pdf = PdfPages('/home/data/archive/%s_Resonator_%d.pdf' % ('StarCryo_5x4_0813f12_Dark',idx))
    res = arch[arch.ridx==idx]
    f0max = res.f_0.max()
    powers = np.unique(res.power_dbm).tolist()
    powers.sort()
    rtemps = np.unique(res.round_temp).tolist()
    rtemps.sort()
    pcolors = plt.cm.spectral(np.linspace(0.1,0.9,len(powers)))
    tcolors = plt.cm.spectral(np.linspace(0.1,0.9,len(rtemps)))
    
    title = 'StarCryo_5x4_0813f12_Dark\nResonator %d ~%.6f MHz' % (idx,f0max)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        f0 = this.f_0
        frac_f0 = f0/f0.max() - 1
        ax.plot(this.end_temp*1000,frac_f0,'.-',color=c,label=('%.1f dBm' % power))
    ax.grid()
    ax.set_xlim(tminmk,tmaxmk)
    ax.legend(loc='lower left',prop=dict(size='small'))
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('Fractional frequency shift')
    pdf.savefig(fig,bbox_inches='tight')
    ax.set_ylim(-5e-5,0)
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        ax.plot(this.end_temp*1000,this.Q_i,'.-',color=c,label=('%.1f dBm' % power))
    ax.grid()
    ax.legend(loc='lower left',prop=dict(size='small'))
    ax.set_xlim(tminmk,tmaxmk)
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('$Q_i$')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        ax.plot(this.end_temp*1000,this.Q_e_real,'.-',color=c,label=('%.1f dBm' % power))
    ax.grid()
    ax.legend(loc='lower right',prop=dict(size='small'))
    ax.set_xlim(tminmk,tmaxmk)
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('$Q_c$')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        ax.plot(this.end_temp*1000,this.Q,'.-',color=c,label=('%.1f dBm' % power))
    ax.grid()
    ax.legend(prop=dict(size='small'))
    ax.set_xlim(tminmk,tmaxmk)
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('$Q_r$')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        ax.plot(this.end_temp*1000,this.noise_250_hz/this.noise_30_khz,'.-',color=c,label=('%.1f dBm' % power))
    ax.legend(prop=dict(size='small'))
    ax.set_ylim(0,20)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('Device noise / Amp noise')    
    pdf.savefig(fig,bbox_inches='tight')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        ax.semilogy(this.end_temp*1000,this.noise_250_hz,'.-',color=c,label=('%.1f dBm' % power))
    ax.legend(prop=dict(size='small'))
    ax.grid()
    ax.set_ylim(0,20)
    ax.set_xlim(tminmk,tmaxmk)
    ax.set_ylim(1e-20,1e-14)
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('Noise at 250 Hz (1/Hz)')
    pdf.savefig(fig,bbox_inches='tight')
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for power in powers:
        c = pcolors[powers.index(power)]
        this = res[res.power_dbm == power]
        this = this.sort(['end_temp'])
        amp_noise_voltsrthz = np.sqrt(4*1.38e-23*4.0*50)
        vread = np.sqrt(50*10**(power/10.0)*1e-3)
        alpha = 1.0
        Qe = np.abs(this.Q_e_real)
        f0_dVdf = 4*vread*alpha*this.Q**2/Qe
        expected_amp_noise = (amp_noise_voltsrthz/f0_dVdf)**2 
        ax.semilogy(this.end_temp*1000,this.noise_30_khz,'.-',color=c,label=('%.1f dBm' % power))
        ax.semilogy(this.end_temp*1000,expected_amp_noise,'--',color=c)
    ax.legend(prop=dict(size='small'))
    ax.set_ylim(0,20)
    ax.set_xlim(tminmk,tmaxmk)
    ax.set_ylim(1e-20,1e-14)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlabel('Temperature (mK)')
    ax.set_ylabel('Noise at 30 kHz (1/Hz)')
    ax.text(0.95,0.1,"Dashed lines show expected amplifier noise level",fontdict=dict(size='small'), ha='right',va='bottom',
            transform=ax.transAxes)
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rtemp in rtemps:
        c = tcolors[rtemps.index(rtemp)]
        this = res[res.round_temp == rtemp]
        this = this.sort(['power_dbm'])
        ax.plot(this.power_dbm,this.Q_i,'.-',color=c,label=('%.1f mK' % (rtemp)))
    ax.legend(loc='upper left',prop=dict(size='xx-small'),ncol=2)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlim(-115,-90)
    ax.set_xlabel('Readout Power (dBm)')
    ax.set_ylabel('$Q_i$')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rtemp in rtemps:
        c = tcolors[rtemps.index(rtemp)]
        this = res[res.round_temp == rtemp]
        this = this.sort(['power_dbm'])
        f0 = this.f_0
        frac_f0 = f0/f0.max() - 1

        ax.plot(this.power_dbm,frac_f0,'.-',color=c,label=('%.1f mK' % (rtemp)))
    ax.legend(loc='lower right',prop=dict(size='xx-small'),ncol=2)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlim(-115,-90)
    ax.set_ylim(-2e-5,0)
    ax.set_xlabel('Readout Power (dBm)')
    ax.set_ylabel('Fractional frequency shift')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rtemp in rtemps:
        c = tcolors[rtemps.index(rtemp)]
        this = res[res.round_temp == rtemp]
        this = this.sort(['power_dbm'])
        ax.plot(this.power_dbm,this.noise_250_hz/this.noise_30_khz,'.-',color=c,label=('%.1f mK' % (rtemp)))
    ax.legend(loc='upper left',prop=dict(size='xx-small'),ncol=2)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlim(-115,-90)
    ax.set_xlabel('Readout Power (dBm)')
    ax.set_ylabel('Device noise / Amp noise') 
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rtemp in rtemps:
        c = tcolors[rtemps.index(rtemp)]
        this = res[res.round_temp == rtemp]
        this = this.sort(['power_dbm'])
        ax.semilogy(this.power_dbm,this.noise_250_hz,'.-',color=c,label=('%.1f mK' % (rtemp)))
    ax.legend(prop=dict(size='xx-small'),ncol=2)        
    ax.set_ylim(1e-20,1e-14)
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlim(-115,-90)
    ax.set_xlabel('Readout Power (dBm)')
    ax.set_ylabel('Noise at 250 Hz (1/Hz)')
    pdf.savefig(fig,bbox_inches='tight')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for rtemp in rtemps:
        c = tcolors[rtemps.index(rtemp)]
        this = res[res.round_temp == rtemp]
        this = this.sort(['power_dbm'])
        ax.semilogy(this.power_dbm,this.noise_30_khz,'.-',color=c,label=('%.1f mK' % (rtemp)))
    ax.legend(prop=dict(size='xx-small'),ncol=2)
    ax.set_ylim(1e-20,1e-14)            
    ax.grid()
    ax.set_title(title,size='small')
    ax.set_xlim(-115,-90)
    ax.set_xlabel('Readout Power (dBm)')
    ax.set_ylabel('Noise at 30 kHz (1/Hz)')
    pdf.savefig(fig,bbox_inches='tight')
    
    for rtemp in rtemps:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for power in powers:
            c = pcolors[powers.index(power)]
            this = res[(res.power_dbm == power) & (res.round_temp == rtemp)]
            if len(this) == 0:
                continue
            this = this.sort(['end_temp'])
            ax.loglog(this.pca_fr.iat[0],this.pca_evals.iat[0][1,:],color=c,label=('%.1f dBm' % power))
        ax.legend(prop=dict(size='small'))
        ax.grid()
        #ax.set_ylim(0,20)
        #ax.set_xlim(tminmk,tmaxmk)
        ax.set_ylim(1e-20,1e-14)
        ax.set_title(title + (' %.1f mK' % rtemp),size='small')
        #ax.set_xlabel('Temperature (mK)')
        #ax.set_ylabel('Noise at 250 Hz (1/Hz)')
        pdf.savefig(fig,bbox_inches='tight')
        
    for power in powers:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for rtemp in rtemps:
            c = tcolors[rtemps.index(rtemp)]
            this = res[(res.power_dbm == power) & (res.round_temp == rtemp)]
            if len(this) == 0:
                continue
            this = this.sort(['end_temp'])
            ax.loglog(this.pca_fr.iat[0],this.pca_evals.iat[0][1,:],color=c,label=('%0.1f mK' % rtemp))
        ax.legend(prop=dict(size='xx-small'))
        ax.grid()
        #ax.set_ylim(0,20)
        #ax.set_xlim(tminmk,tmaxmk)
        ax.set_ylim(1e-20,1e-14)
        ax.set_title(title + (' %.1f dBm' % power),size='small')
        #ax.set_xlabel('Temperature (mK)')
        #ax.set_ylabel('Noise at 250 Hz (1/Hz)')
        pdf.savefig(fig,bbox_inches='tight')

    pdf.close()
    plt.close('all')
    
